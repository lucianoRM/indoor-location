#ifndef BEACON_CONFIG_H
#define BEACON_CONFIG_H

#define STR_INDIR(x) #x
#define STR(x) STR_INDIR(x)

//WIFI
#define WIFI_SSID "indoor"
#define WIFI_PASS "location"

//SERVER
#define HTTP_HOST "10.42.0.1"
#define HTTP_PORT 8082

#define LOG_ULR "/log"

#define ANCHORS_URL "/anchors"
#define SIGNAL_EMITTERS_URL "/signal_emitters"
#define SIGNAL_URL_UNFORMATTED "/signal_emitters/%s/signal"

//BLE
#define BLE_SCANNING_FREQUENCY_MS 30000000 //dont do anything
#define BLE_SCANNING_LENGTH_MS 10000 //5 secs

//SYSTEM
#define BEACON_ID 4
#define BEACON_ID_STRING STR(BEACON_ID)
#define MEDIUM_COEFF_KEY "MEDIUM_COEF_BY_" BEACON_ID_STRING
#define POWER_AVERAGE_KEY "PWR_AVG_BY_" BEACON_ID_STRING

//LOG
#define LOG_TAG "BEACON-"BEACON_ID_STRING

#endif //BEACON_CONFIG_H
