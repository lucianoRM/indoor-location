#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <freertos/semphr.h>
#include <esp_log.h>
#include "driver/gpio.h"
#include "light.h"

#define LIGHT_PIN GPIO_NUM_2
#define DELAY_BETWEEN_BURSTS 500
#define IN_BURST_DELAY 200
#define UNINITIALIZED -1
#define OFF 0
#define ON 1

static int light_status = UNINITIALIZED;
static long light_delay = DELAY_BETWEEN_BURSTS;
static int burst_total = 1;
static SemaphoreHandle_t lock = NULL;

static TaskHandle_t blinkHandle = NULL;

static void _toggle();

static void _blink(void* parameters) {

    int burst_count = 0;
    while(1) {
        _toggle();
        xSemaphoreTake(lock, portMAX_DELAY);
        long total_bursts = burst_total;
        long delay = light_delay/portTICK_PERIOD_MS;
        int status = light_status;
        xSemaphoreGive(lock);
        if(++burst_count < total_bursts) {
            delay = IN_BURST_DELAY/portTICK_PERIOD_MS;
        }else if(status == OFF){
            burst_count = 0;
        }
        vTaskDelay(delay);
    }

}

void _change_mode(int mode) {
    bool tookLock = false;
    if(lock) {
        xSemaphoreTake(lock,portMAX_DELAY);
        tookLock = true;
    }
    if(light_status == UNINITIALIZED) {
        gpio_pad_select_gpio(LIGHT_PIN);
        gpio_set_direction(LIGHT_PIN, GPIO_MODE_OUTPUT);
    }
    gpio_set_level(LIGHT_PIN, mode);
    light_status = mode;
    if(lock && tookLock) {
        xSemaphoreGive(lock);
    }
}

static void _toggle() {
    if(light_status == ON) {
        turn_off_led();
    }else {
        turn_on_led();
    }
}

void turn_on_led() {
    _change_mode(ON);
}

void turn_off_led() {
    _change_mode(OFF);
}

void start_blinking_led() {
    if(!blinkHandle) {
        lock = xSemaphoreCreateBinary();
        xSemaphoreGive(lock);
        xTaskCreate(&_blink,"BLINK",configMINIMAL_STACK_SIZE,NULL,5,&blinkHandle);
    }
    if(eTaskGetState(blinkHandle) == eSuspended) {
        vTaskResume(blinkHandle);
    }
}

void stop_blinking_led() {
    ESP_LOGD("LIGHT", "CHECKING FOR SUSPENSION");
    
    if(blinkHandle && (eTaskGetState(blinkHandle) != eSuspended)) {
        ESP_LOGD("LIGHT", "SUSPENDED");
        vTaskSuspend(blinkHandle);
        ESP_LOGD("LIGHT", "SUSPENED");
    }
}

void set_burst_mode_led(int burst_length, long delay) {
    if(lock) {
        xSemaphoreTake(lock, portMAX_DELAY);
        light_delay = delay;
        burst_total = burst_length * 2; //one for off and one for on
        xSemaphoreGive(lock);
    }
}

void set_blink_mode_led(long delay) {
    set_burst_mode_led(0, delay);
}



