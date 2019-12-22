#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <string.h>
#include "wifi.h"
#include "esp_system.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "config.h"
#include "http.h"
#include "parser.h"
#include "ble.h"
#include "light.h"
#include "utils.h"
#include "button.h"

#define TAG "BEACON"
#define BLINK_DELAY 500

static int ble_power_level = 2;

llist* get_located_signal_emitters() {
    http_response_t se_response = get(SIGNAL_EMITTERS_URL);
    if (se_response.data) {
        ESP_LOGD(TAG, "GOT SEs: %s", se_response.data);
        ESP_LOGD(TAG, "About to parse ses");
        llist* signal_emitters_container = parse_signal_emitters(se_response.data);
        ESP_LOGD(TAG, "parsed ses");
        ESP_LOGD(TAG, "About to free se_response");
        free_response(&se_response);
        ESP_LOGD(TAG, "se_response freed");
        return signal_emitters_container;
    }
    return NULL;
}

void put_sensed_values(signal_emitter_t* se) {
    char path[strlen(SIGNAL_URL_UNFORMATTED) + strlen(se->id)];
    sprintf(path, SIGNAL_URL_UNFORMATTED, se->id);

    char* body = build_signal_json(se->signal);
    http_response_t response = put(path, body, strlen(body));

    if(response.code != 200) {
        ESP_LOGW(TAG, "HTTP ERROR %d UPDATING SE: %s, %s", response.code, se->id, response.data);
    }
    free_response(&response);
    free(body);
}

void put_all_sensed_values(llist* ses) {
    signal_emitter_t* se;
    FOREACH(se, ses) {
        ESP_LOGI("BLE", "putting %s: %f", se->id, se->signal->coeff);
        if(se->signal->coeff > 0.0f) {
            put_sensed_values(se);
        }
    }
}

void calibrate() {
    stop_blinking_led();
    turn_on_led();

    //Get signal emitters
    llist* ses = get_located_signal_emitters();
    if(ses) {
        signal_emitter_t* se;
        FOREACH(se, ses) {
            ESP_LOGD(TAG, "se: %s, x: %f, y: %f", se->id, se->x, se->y);
            ESP_LOGD(TAG, "signal coef: %f", se->signal->coeff);
        }
        //ADVERTISING*******************************************
        //SCANNING**********************************************
        compute_coefficients(ses, BLE_SCANNING_LENGTH_MS);
        //SCANNING**********************************************
        //ADVERTISING*******************************************
        put_all_sensed_values(ses);

        free_signal_emitters(ses);
    }

    turn_off_led();
    start_blinking_led(250);
}

//void loop() {
//    while(true) {
//
//        //ADVERTISING*************************************
//        turn_off_led();
//        start_blinking_led();
//
//
//        int random = 0x01;
//        //If the last bit is 1, loop again, else, run a scan cycle.
//        //Start with 1 so that there is at least one advertising cycle after after every scanning
//        //Add a random value to the advertising cycle to reduce overlapping
//        while(random & 0x01) {
//            //+ up to 25%
//            int random_delay = random % (BLE_SCANNING_FREQUENCY_MS / 4);
//            uint32_t delay = (BLE_SCANNING_FREQUENCY_MS + random_delay)/portTICK_PERIOD_MS;
//            vTaskDelay(delay);
//            random = esp_random();
//        }
//
//        stop_blinking_led();
//        turn_on_led();
//
//
//    }
//}

void change_ble_power() {
    ESP_LOGI("BUTTON", "ON PRESS EXECUTED");
    if(++ble_power_level >= 3) {
        ble_power_level = 0;
    }
    switch (ble_power_level) {
        case 0:
            set_advertising_power(MIN_POWER);
            break;
        case 1:
            set_advertising_power(MEDIUM_POWER);
            break;
        case 2:
            set_advertising_power(MAX_POWER);
            break;
    }
    set_burst_mode_led(ble_power_level + 1, BLINK_DELAY);
}

void app_main() {
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    //Connect to wifi
    connect(WIFI_SSID, WIFI_PASS);

    //Start ble
    start_bluetooth_module(BEACON_ID);

    button_on_press(&change_ble_power);
    button_on_long_press(&calibrate);
    button_start();

    start_blinking_led();
    set_burst_mode_led(ble_power_level + 1, BLINK_DELAY);
}