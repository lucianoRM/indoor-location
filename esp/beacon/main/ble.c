#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include "esp_ibeacon_api.h"
#include "esp_bt.h"
#include "esp_gap_ble_api.h"
#include "esp_bt_main.h"
#include "esp_bt_defs.h"
#include "esp_log.h"
#include "ble.h"
#include "signal_utils.h"
#include "config.h"
#include "utils.h"
#include "list.h"

#define MIN_REQUIRED_MEASUREMENTS 15
#define MAX_TIME_BETWEEN_MEASUREMENTS_US BLE_SCANNING_LENGTH_MS * 1000 //5 seconds


static const uint8_t uuid_zeros[ESP_UUID_LEN_128] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                                     0x00, 0x00, 0x00, 0x00, 0x00};

static const char* TAG = "BLE";

static llist* beacons_data;

extern esp_ble_ibeacon_vendor_t vendor_config;

///Declare static functions
static void esp_gap_cb(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t* param);

static uint64_t get_id(esp_ble_ibeacon_t* ibeacon_data);

static ble_data_t* get_ble_data(char* id);

static void add_sensed_power(char* id, int power);

static float get_power_average(ble_data_t* ble_data);

static esp_ble_scan_params_t ble_scan_params = {
        .scan_type              = BLE_SCAN_TYPE_ACTIVE,
        .own_addr_type          = BLE_ADDR_TYPE_PUBLIC,
        .scan_filter_policy     = BLE_SCAN_FILTER_ALLOW_ALL,
        .scan_interval          = 0x50,
        .scan_window            = 0x30,
        .scan_duplicate         = BLE_SCAN_DUPLICATE_DISABLE
};

static esp_ble_adv_params_t ble_adv_params = {
        .adv_int_min        = 0x20,
        .adv_int_max        = 0x40,
        .adv_type           = ADV_TYPE_NONCONN_IND,
        .own_addr_type      = BLE_ADDR_TYPE_PUBLIC,
        .channel_map        = ADV_CHNL_ALL,
        .adv_filter_policy = ADV_FILTER_ALLOW_SCAN_ANY_CON_ANY,
};

static uint64_t get_id(esp_ble_ibeacon_t* ibeacon_data) {
    int first_position = ESP_UUID_LEN_128 / 2;
    uint64_t uuid = 0;
    for (int i = first_position; i < ESP_UUID_LEN_128; i++) {
        uint64_t valuebuffer = ibeacon_data->ibeacon_vendor.proximity_uuid[i];
        valuebuffer <<= ESP_UUID_LEN_128 - i - 1;
        uuid |= valuebuffer;
    }
    return uuid;
}

//Get the ble_data object from the container.
// The container should already be populated. If the data does not exists, return NULL
static ble_data_t* get_ble_data(char* id) {
    ble_data_t* tmp;
    FOREACH(tmp, beacons_data) {
        if (!strcmp(tmp->id, id)) {
            return tmp;
        }
    }
    return NULL;
}

static float get_power_average(ble_data_t* ble_data) {
    unsigned int total_values =
            ble_data->total_measurements > MEASUREMENTS_WINDOW ? MEASUREMENTS_WINDOW : ble_data->total_measurements;
    float sum = 0.0f;
    for (unsigned int i = 0; i < total_values; i++) {
        sum += ble_data->measurements[i];
    }
    float result = -(sum / total_values);//Transform to negative again.
    ESP_LOGI("BLE", "Computing average for SE: %s, got: %.2f after %d measurements", ble_data->id, result, total_values);
    return result;
}

//It will add the new sensed power unless the array is already full
static void add_sensed_power(char* id, int power) {
    ble_data_t* ble_data = get_ble_data(id);
    //Check for NULL
    if (ble_data) {
        uint8_t positive_power = -(power); //Measured power will always be negative, transform to positive.
        unsigned int index = ble_data->total_measurements % MEASUREMENTS_WINDOW;
        ble_data->total_measurements++;
        ble_data->measurements[index] = positive_power;
        ble_data->last_updated = esp_timer_get_time();
    }
}

static void esp_gap_cb(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t* param) {
    esp_err_t err;

    switch (event) {
        case ESP_GAP_BLE_ADV_DATA_RAW_SET_COMPLETE_EVT: {
            esp_ble_gap_stop_scanning();
            break;
        }
        case ESP_GAP_BLE_SCAN_PARAM_SET_COMPLETE_EVT: {
            //the unit of the duration is second, 0 means scan permanently
            esp_ble_gap_stop_advertising();
            break;
        }
        case ESP_GAP_BLE_SCAN_START_COMPLETE_EVT:
            //scan start complete event to indicate scan start successfully or failed
            if ((err = param->scan_start_cmpl.status) != ESP_BT_STATUS_SUCCESS) {
                ESP_LOGE(TAG, "Scan start failed: %s", esp_err_to_name(err));
            }
            break;
        case ESP_GAP_BLE_ADV_START_COMPLETE_EVT:
            //adv start complete event to indicate adv start successfully or failed
            if ((err = param->adv_start_cmpl.status) != ESP_BT_STATUS_SUCCESS) {
                ESP_LOGE(TAG, "Adv start failed: %s", esp_err_to_name(err));
            }
            break;
        case ESP_GAP_BLE_SCAN_RESULT_EVT: {
            esp_ble_gap_cb_param_t* scan_result = (esp_ble_gap_cb_param_t*) param;
            switch (scan_result->scan_rst.search_evt) {
                case ESP_GAP_SEARCH_INQ_RES_EVT:
                    /* Search for BLE iBeacon Packet */
                    if (esp_ble_is_ibeacon_packet(scan_result->scan_rst.ble_adv, scan_result->scan_rst.adv_data_len)) {
                        esp_ble_ibeacon_t* ibeacon_data = (esp_ble_ibeacon_t*) (scan_result->scan_rst.ble_adv);
                        uint64_t id = get_id(ibeacon_data);
                        char id_string[64];
                        sprintf(id_string, "%llu", id);
                        add_sensed_power(id_string, scan_result->scan_rst.rssi);
                        ESP_LOGD(TAG, "TESTING UUID: %s", id_string);
                        ESP_LOGD(TAG, "RSSI of packet:%d dbm", scan_result->scan_rst.rssi);
                    }
                    break;
                default:
                    break;
            }
            break;
        }

        case ESP_GAP_BLE_SCAN_STOP_COMPLETE_EVT:
            if ((err = param->scan_stop_cmpl.status) != ESP_BT_STATUS_SUCCESS) {
                ESP_LOGE(TAG, "Scan stop failed: %s", esp_err_to_name(err));
            } else {
                ESP_LOGI(TAG, "Stop scan successfully");
            }
            esp_ble_gap_start_advertising(&ble_adv_params);
            break;

        case ESP_GAP_BLE_ADV_STOP_COMPLETE_EVT:
            if ((err = param->adv_stop_cmpl.status) != ESP_BT_STATUS_SUCCESS) {
                ESP_LOGE(TAG, "Adv stop failed: %s", esp_err_to_name(err));
            } else {
                ESP_LOGD(TAG, "Stop adv successfully");
            }
            esp_ble_gap_start_scanning(0);
            break;

        default:
            break;
    }
}

void ble_ibeacon_appRegister(void) {
    esp_err_t status;

    ESP_LOGD(TAG, "register callback");

    //register the scan callback function to the gap module
    if ((status = esp_ble_gap_register_callback(esp_gap_cb)) != ESP_OK) {
        ESP_LOGE(TAG, "gap register error: %s", esp_err_to_name(status));
        return;
    }

}

void ble_ibeacon_init(void) {
    esp_bluedroid_init();
    esp_bluedroid_enable();
    ble_ibeacon_appRegister();
}

void free_data() {
    ble_data_t* tmp;
    FOREACH(tmp, beacons_data) {
        free(tmp->id);
        free(tmp);
    }
    llist_destroy(beacons_data);
}

void start_advertising(uint8_t id) {

    //configure beacons base data
    esp_ble_ibeacon_t ibeacon_adv_data;
    esp_err_t status = esp_ble_config_ibeacon_data(&vendor_config, &ibeacon_adv_data);

    //override id
    memcpy(ibeacon_adv_data.ibeacon_vendor.proximity_uuid, uuid_zeros, sizeof(uuid_zeros) - sizeof(uint8_t));
    memcpy(&(ibeacon_adv_data.ibeacon_vendor.proximity_uuid[ESP_UUID_LEN_128 - 1]), &id, sizeof(uint8_t));

    //Once the parameters are set, the beacon should start advertising
    if (status == ESP_OK) {
        ESP_LOGD(TAG, "Set adv data");
        ESP_LOG_BUFFER_HEX(TAG, ibeacon_adv_data.ibeacon_vendor.proximity_uuid, ESP_UUID_LEN_128);
        esp_ble_gap_config_adv_data_raw((uint8_t*) &ibeacon_adv_data, sizeof(ibeacon_adv_data));
    } else {
        ESP_LOGE(TAG, "Config iBeacon data failed: %s\n", esp_err_to_name(status));
    }
}

//Compare times, they are un microseconds
bool are_times_close(int64_t now, int64_t last_measured) {
    return (now - last_measured) < MAX_TIME_BETWEEN_MEASUREMENTS_US;
}

void compute_coefficients(llist* signal_emitters, int time_ms) {
    ESP_LOGI(TAG, "COMPUTING COEFFICIENTS");
    //Configure global beacons data with the information from the signal_emitters
    ESP_LOGI(TAG, "Configuring beacons data, expecting %d beacons", signal_emitters->size);

    signal_emitter_t* myself = NULL;
    signal_emitter_t* tmp_se;

    FOREACH(tmp_se, signal_emitters) {
        //set my position
        if (!strcmp(tmp_se->id, BEACON_ID_STRING)) {
            myself = tmp_se;
        }
        //if not present add it
        if (!get_ble_data(tmp_se->id)) {
            ble_data_t* tmp = malloc(sizeof(ble_data_t));
            char* string_id = malloc(sizeof(char) * 2); //one number and \0
            strcpy(string_id, tmp_se->id);
            ESP_LOGI(TAG, "Adding: %c %c", string_id[0], string_id[1]);
            tmp->id = string_id;
            tmp->total_measurements = 0;
            llist_insert(beacons_data, tmp);
        }

    }
    //Once parameters are set, the beacon will stop advertising and it will start sensing.
    esp_ble_gap_set_scan_params(&ble_scan_params);

    //Block for time_ms and return
    uint32_t delay = time_ms / portTICK_PERIOD_MS;
    vTaskDelay(delay);

    //Return to advertising mode
    esp_ble_gap_stop_scanning();

    //Copy computed values to container
//    log_in_server("Found only %d SEs", signal_emitters->size);
    FOREACH(tmp_se, signal_emitters) {
        if (tmp_se == myself) continue;
        int64_t now = esp_timer_get_time();
        ble_data_t* ble_data = get_ble_data(tmp_se->id);
        if (ble_data && myself && are_times_close(now, ble_data->last_updated)) {
            float power_avg = get_power_average(ble_data);
            float coeff = compute_coefficient(tmp_se, myself->x, myself->y, power_avg);
//            log_in_server("SE ID: %s, PowAVG: %.2f, Nmeasurements: %d, Computed coeff: %.2f", tmp_se->id, power_avg,
//                          ble_data->total_measurements, coeff);
            tmp_se->signal->power_average = power_avg;
            tmp_se->signal->coeff = coeff;
        } else {
            ESP_LOGW(TAG, "BLE with id: %s, not found", tmp_se->id);
        }
    }
}

void set_advertising_power(esp_power_level_t power_level) {
    esp_err_t set_power_result = esp_ble_tx_power_set(ESP_BLE_PWR_TYPE_ADV, power_level);
    if(set_power_result != ESP_OK) {
        ESP_LOGE(TAG, "Could not set adv power!");
    }
    ESP_LOGE(TAG, "BLE ADV POWER IS: %d", esp_ble_tx_power_get(ESP_BLE_PWR_TYPE_ADV));
}

void start_bluetooth_module(uint8_t id) {
    ESP_ERROR_CHECK(esp_bt_controller_mem_release(ESP_BT_MODE_CLASSIC_BT));

    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
    esp_bt_controller_init(&bt_cfg);
    esp_bt_controller_enable(ESP_BT_MODE_BLE);
    esp_err_t set_power_result = esp_ble_tx_power_set(ESP_BLE_PWR_TYPE_ADV, ESP_PWR_LVL_P9);
    if(set_power_result != ESP_OK) {
        ESP_LOGE(TAG, "Could not set adv power!");
    }
    set_power_result = esp_ble_tx_power_set(ESP_BLE_PWR_TYPE_SCAN, ESP_PWR_LVL_P9);
    if(set_power_result != ESP_OK) {
        ESP_LOGE(TAG, "Could not set scanning power!");
    }
    ESP_LOGE(TAG, "BLE ADV POWER IS: %d", esp_ble_tx_power_get(ESP_BLE_PWR_TYPE_ADV));
    ESP_LOGE(TAG, "BLE SCAN POWER IS: %d", esp_ble_tx_power_get(ESP_BLE_PWR_TYPE_SCAN));

    ble_ibeacon_init();

    start_advertising(id);

    beacons_data = llist_create();
}