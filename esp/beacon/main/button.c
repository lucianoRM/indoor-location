#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <esp_log.h>
#include "button.h"

#define DEBOUNCING_TIME 10 //milliseconds
#define DEBOUNCING_TICKS DEBOUNCING_TIME/portTICK_PERIOD_MS

static void button_poller_task(void* params);

static void (*onPressCallback)() = NULL;
static void (*onLongPressCallback)() = NULL;

static TaskHandle_t buttonTaskHandle = NULL;

void execute_long_press() {
    if(onLongPressCallback) {
        onLongPressCallback();
    }
}

void execute_press() {
    if(onPressCallback) {
        onPressCallback();
    }
}

bool long_press() {
    int timePressed = 0;
    while(gpio_get_level(BUTTON_PIN) == PRESSED) {
        if(timePressed >= LONG_PRESS_DELAY) {
            execute_long_press();
            return true;
        }
        vTaskDelay(DEBOUNCING_TICKS);
        timePressed += DEBOUNCING_TICKS;
    }
    return false;
}

static void button_poller_task(void* args) {
    while(1) {
        ulTaskNotifyTake(pdTRUE,
                         portMAX_DELAY );
        if(!long_press() && gpio_get_level(BUTTON_PIN) == RELEASED) {
            execute_press();
        }
        vTaskDelay(DEBOUNCING_TICKS);
    }
}

void button_pressed_interrupt(void *args) {
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    vTaskNotifyGiveFromISR(buttonTaskHandle,
                           &xHigherPriorityTaskWoken);
    portYIELD_FROM_ISR();
}

void button_start() {
    gpio_config_t btn_config;
    btn_config.intr_type = GPIO_INTR_NEGEDGE; 	//Enable interrupt on both rising and falling edges
    btn_config.mode = GPIO_MODE_INPUT;        	//Set as Input
    btn_config.pin_bit_mask = (1 << BUTTON_PIN); //Bitmask
    btn_config.pull_up_en = GPIO_PULLUP_DISABLE; 	//Disable pullup
    btn_config.pull_down_en = GPIO_PULLDOWN_ENABLE; //Enable pulldown
    gpio_config(&btn_config);

    //Configure interrupt and add handler
    gpio_install_isr_service(0);						//Start Interrupt Service Routine service
    gpio_isr_handler_add(BUTTON_PIN, button_pressed_interrupt, NULL); //Add handler of interrupt

    if(!buttonTaskHandle) {
        xTaskCreate(&button_poller_task, "BUTTON_TASK", 4096, NULL, 5, &buttonTaskHandle);
    }
}
void button_on_press(void (*on_press)(char*)) {
    onPressCallback = on_press;
}

void button_on_long_press(void (*on_long_press)(char*)) {
    onLongPressCallback = on_long_press;
}