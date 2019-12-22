#ifndef BEACON_BUTTON_H
#define BEACON_BUTTON_H

#include "driver/gpio.h"
#include <freertos/task.h>

#define BUTTON_PIN GPIO_NUM_0
#define LONG_PRESS_SECONDS 3
#define LONG_PRESS_MILLIS LONG_PRESS_SECONDS*1000
#define LONG_PRESS_DELAY (LONG_PRESS_MILLIS/portTICK_PERIOD_MS)
#define PRESSED 0
#define RELEASED !PRESSED


/**
 * Function to call when button is called
 */
void button_on_press(void (*on_press)(char*));

/**
 * Function to call when button is pressed for N seconds
 * @param on_long_press
 */
void button_on_long_press(void (*on_long_press)(char*));

/**
 * start button logic. Configuration should not be called after this is executed
 */
void button_start();

#endif //BEACON_BUTTON_H
