# ESP32 BLE Beacon

This is the C source code for a simple BLE Beacon implemented using de ESP32 SDK.

>It is assumed that the ESP-IDF is already configured in the computer and any example proyect has been tested in the board owner, otherwise, check: 
https://docs.espressif.com/projects/esp-idf/en/latest/get-started/index.html

Before the proyect is built, configure the required parameters in the file `main/config.h` 
* __WIFI_SSID__ The WiFi SSID to connect to.
* __WIFI_PASS__ The WiFi network password.
* __HTTP_HOST__ The Server IP.
* __HTTP_PORT__ The Server port.
* __BEACON_ID__ The ID that this beacon will have in the system.

All this code was develped using a **ESP-WROOM-32** board, if using a different one, this is not guaranteed to work. 

### Build the project
```
idf.py build
```

### Flash the project
```
idf.py -p (PORT) flash
``` 

Once the code start running, the blue LED from the board should start blinking.