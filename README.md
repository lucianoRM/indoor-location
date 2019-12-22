# Android Indoor Location Framework
This repository contains all the code that is part of an indoor location framework for Android applications development.

The code is organized as follows:

* `/server` An HTTP server built with Python that handles both the storage and the logic for positioning users in the system
* `/android/location` All related to the Android development framework. It contains 3 parts:
  * `/api` The framework API and internal logic. This is what should be used for developing an app using this framework.
  * `/impl` Some implementation logic that uses the framework api, to avoid having to build everything from scratch.
  * `/app` A test application that uses the ESP32 beacons. 
* `/esp/beacon` An implementation example with the ESP-WROOM-32 board acting as BLE beacons. Source code in C using the ESP-IDF SDK.
