#ifndef BEACON_BLE_H
#define BEACON_BLE_H

#include "parser.h"
#include "esp_bt.h"

#define MEASUREMENTS_WINDOW 50

#define MIN_POWER ESP_PWR_LVL_N9
#define MEDIUM_POWER ESP_PWR_LVL_N0
#define MAX_POWER ESP_PWR_LVL_P9

/**
 * Where to collect information for every beacon sensed.
 */
typedef struct ble_data {
    char* id;
    uint8_t measurements[MEASUREMENTS_WINDOW]; //Absolute values should not be bigger than 255
    unsigned int total_measurements;
    int64_t last_updated;
} ble_data_t;

/**
 * Change to scanning mode and compute coefficients of all possible signal emitters.
 * Then return to advertising mode
 * @param signal_emitters
 * @param time to scan in millis
 */
void compute_coefficients(llist* signal_emitters, int time_ms);

void set_advertising_power(esp_power_level_t level);

/**
 * Start the BLE module.
 * After this call, the module will start advertising, unless interrupted by the compute_coefficients() call;
 *
 * For now we represent the ids with an 8 bit number
 */
void start_bluetooth_module(uint8_t id);

#endif //BEACON_BLE_H
