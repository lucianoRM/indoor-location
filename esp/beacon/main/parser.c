#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <esp_log.h>
#include "parser.h"
#include "cJSON.h"
#include "config.h"
#include "list.h"

llist* parse_anchors(char* json_string) {
    cJSON* anchors_object = cJSON_Parse(json_string);

    cJSON* anchor_placeholder;
    llist* anchors = NULL;
    if(cJSON_IsArray(anchors_object)) {
        anchors = llist_create();
        cJSON_ArrayForEach(anchor_placeholder, anchors_object) {
            cJSON* anchor_id_json = cJSON_GetObjectItemCaseSensitive(anchor_placeholder, "id");
            cJSON* position_json = cJSON_GetObjectItemCaseSensitive(anchor_placeholder, "position");
            cJSON* position_x_json = cJSON_GetObjectItemCaseSensitive(position_json, "x");
            cJSON* position_y_json = cJSON_GetObjectItemCaseSensitive(position_json, "y");

            cJSON* signal_emitters = cJSON_GetObjectItemCaseSensitive(anchor_placeholder, "signal_emitters");
            cJSON* signal_emitter_placeholder;
            llist* signal_emitters_container = llist_create();
            if(cJSON_IsObject(signal_emitters)) {
                cJSON_ArrayForEach(signal_emitter_placeholder, signal_emitters) {
                    char* signal_emitter_id = malloc(sizeof(char) * (strlen(signal_emitter_placeholder->string) + 1)); //account for \0
                    strcpy(signal_emitter_id, signal_emitter_placeholder->string);
                    llist_insert(signal_emitters_container, signal_emitter_id);
                }
            }
            char* anchor_id = malloc(sizeof(char) * (strlen(anchor_id_json->valuestring) + 1)); //account for \0
            strcpy(anchor_id, anchor_id_json->valuestring);
            anchor_t* anchor = malloc(sizeof(anchor_t));
            anchor->id = anchor_id;
            anchor->x = position_x_json->valuedouble;
            anchor->y = position_y_json->valuedouble;
            anchor->signal_emitter_ids = signal_emitters_container;
            llist_insert(anchors, anchor);
        }
    }
    cJSON_Delete(anchors_object);
    return anchors;
}

void free_anchors(llist* anchors_list) {
    anchor_t* tmp_anchor;
    FOREACH(tmp_anchor, anchors_list) {
        //free id
        free(tmp_anchor->id);

        llist* signal_emitters = tmp_anchor->signal_emitter_ids;
        char* tmp_se_id;
        FOREACH(tmp_se_id, signal_emitters) {
            free(tmp_se_id);
        }

        llist_destroy(signal_emitters);

        free(tmp_anchor);
    }
    llist_destroy(anchors_list);
}

llist* parse_signal_emitters(char* json_string) {
    cJSON* signal_emitters_object = cJSON_Parse(json_string);

    cJSON* signal_emitter_placeholder;

    llist* signal_emitters = NULL;
    if(cJSON_IsArray(signal_emitters_object)) {
        signal_emitters = llist_create();
        cJSON_ArrayForEach(signal_emitter_placeholder, signal_emitters_object) {
            cJSON* signal_emitter_id_json = cJSON_GetObjectItemCaseSensitive(signal_emitter_placeholder, "id");
            char* signal_emitter_id = malloc(sizeof(char) * (strlen(signal_emitter_id_json->valuestring) + 1)); //account for \0
            strcpy(signal_emitter_id, signal_emitter_id_json->valuestring);

            signal_emitter_t* signal_emitter = malloc(sizeof(signal_emitter_t));
            signal_emitter->id = signal_emitter_id;

            cJSON* position_json = cJSON_GetObjectItemCaseSensitive(signal_emitter_placeholder, "position");
            cJSON* position_x_json = cJSON_GetObjectItemCaseSensitive(position_json, "x");
            cJSON* position_y_json = cJSON_GetObjectItemCaseSensitive(position_json, "y");
            signal_emitter->x = position_x_json->valuedouble;
            signal_emitter->y = position_y_json->valuedouble;

            cJSON* signal_json = cJSON_GetObjectItem(signal_emitter_placeholder, "signal");
            cJSON* signal_base_power_json = cJSON_GetObjectItem(signal_json, "MAX_POWER");
            signal_t* signal = malloc(sizeof(signal_t));
            signal->base_power = atoi(signal_base_power_json->valuestring);
            signal->coeff = 0; //Set it as by default. It will later be populated.
            signal_emitter->signal = signal;

            llist_insert(signal_emitters, signal_emitter);
        }
    }
    cJSON_Delete(signal_emitters_object);
    return signal_emitters;
}

void free_signal_emitters(llist* signal_emitters_list) {
    signal_emitter_t* tmp_signal_emitter;
    FOREACH(tmp_signal_emitter, signal_emitters_list) {
        free(tmp_signal_emitter->id);
        free(tmp_signal_emitter->signal);
        free(tmp_signal_emitter);
    }
    llist_destroy(signal_emitters_list);
}

signal_emitter_t* get_signal_emitter_with_id(llist* signal_emitters_list, char* id) {
    signal_emitter_t* tmp_se;
    FOREACH(tmp_se, signal_emitters_list) {
        if(!strcmp(tmp_se->id, id)) {
            return tmp_se;
        }
    }
    return NULL;
}

char* build_signal_json(signal_t* signal) {
    cJSON* signal_json = cJSON_CreateObject();

    char coeff_buffer[10];
    sprintf(coeff_buffer, "%.2f", signal->coeff);
    cJSON_AddItemToObject(signal_json, MEDIUM_COEFF_KEY, cJSON_CreateString(coeff_buffer));

    char pwr_avg_buffer[10];
    sprintf(pwr_avg_buffer, "%.2f", signal->power_average);
    cJSON_AddItemToObject(signal_json, POWER_AVERAGE_KEY, cJSON_CreateString(pwr_avg_buffer));

    char* signal_string = cJSON_Print(signal_json);
    cJSON_Delete(signal_json);
    return signal_string;
}
