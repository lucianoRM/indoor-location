#include <cJSON.h>
#include "config.h"
#include "http.h"
#include <string.h>
#include <stdlib.h>
#include <stdarg.h>
#include <stdio.h>

void log_in_server(char* message, ...) {
    char buffer[500];
    va_list args;
    va_start (args, message);
    vsprintf(buffer,message, args);
    va_end (args);
    cJSON* log = cJSON_CreateObject();
    cJSON_AddItemToObject(log, "tag", cJSON_CreateString(LOG_TAG));
    cJSON_AddItemToObject(log, "message", cJSON_CreateString(buffer));
    char* log_string = cJSON_Print(log);
    cJSON_Delete(log);
    post(LOG_ULR, log_string, strlen(log_string));
    free(log_string);
}
