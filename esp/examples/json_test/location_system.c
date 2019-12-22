#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "location_system.h"
#include "cJSON.h"

container_t parse_anchors(char* json_string) {
    cJSON* anchors_object = cJSON_Parse(json_string);

    cJSON* anchor_placeholder;

    int total_anchors = 0;
    anchor_t* anchors;
    if(cJSON_IsArray(anchors_object)) {
        total_anchors = cJSON_GetArraySize(anchors_object);
        anchors = malloc(sizeof(anchor_t) * total_anchors);
        int anchor_position = 0;
        cJSON_ArrayForEach(anchor_placeholder, anchors_object) {
            cJSON* anchor_id_json = cJSON_GetObjectItemCaseSensitive(anchor_placeholder, "id");
            cJSON* position_json = cJSON_GetObjectItemCaseSensitive(anchor_placeholder, "position");
            cJSON* position_x_json = cJSON_GetObjectItemCaseSensitive(position_json, "x");
            cJSON* position_y_json = cJSON_GetObjectItemCaseSensitive(position_json, "y");

            cJSON* signal_emitters = cJSON_GetObjectItemCaseSensitive(anchor_placeholder, "signal_emitters");
            cJSON* signal_emitter_placeholder;
            container_t signal_emitters_container = {
                    .size = 0
            };
            if(cJSON_IsObject(signal_emitters)) {
                int total_signal_emitters = cJSON_GetArraySize(signal_emitters);
                char** signal_emitters_ids = malloc(total_signal_emitters * sizeof(char*)); //the ids of the signal emitters
                int signal_emitter_position = 0;
                cJSON_ArrayForEach(signal_emitter_placeholder, signal_emitters) {
                    char* signal_emitter_id = malloc(sizeof(char) * (strlen(signal_emitter_placeholder->string) + 1)); //account for \0
                    strcpy(signal_emitter_id, signal_emitter_placeholder->string);
                    signal_emitters_ids[signal_emitter_position] = signal_emitter_id;
                    signal_emitter_position++;
                }
                signal_emitters_container.first = signal_emitters_ids;
                signal_emitters_container.size = total_signal_emitters;
            }
            char* anchor_id = malloc(sizeof(char) * (strlen(anchor_id_json->valuestring) + 1)); //account for \0
            strcpy(anchor_id, anchor_id_json->valuestring);
            anchor_t anchor = {
                    .id = anchor_id,
                    .x = position_x_json->valuedouble,
                    .y = position_y_json->valuedouble,
                    .signal_emitter_ids = signal_emitters_container
            };
            anchors[anchor_position] = anchor;
            anchor_position++;
        }
    }
    cJSON_Delete(anchors_object);
    container_t anchors_container = {
            .first = anchors,
            .size = total_anchors,
    };
    return anchors_container;
}

void free_anchors(anchor_t* first, int size) {
    int i = 0;
    for(;i< size; i++) {
        anchor_t* anchor = first + i;

        //free id
        free(anchor->id);

        container_t signal_emitters = anchor->signal_emitter_ids;
        int j = 0;
        for(; j < signal_emitters.size; j++) {
            char* signal_emitter_id = *((char**)signal_emitters.first + j);
            free(signal_emitter_id);
        }

        free(signal_emitters.first);
    }
    free(first);
}

container_t parse_signal_emitters(char* json_string) {
    cJSON* signal_emitters_object = cJSON_Parse(json_string);

    cJSON* signal_emitter_placeholder;

    int total_signal_emitters = 0;
    signal_emitter_t* signal_emitters = NULL;
    if(cJSON_IsArray(signal_emitters_object)) {
        total_signal_emitters = cJSON_GetArraySize(signal_emitters_object);
        signal_emitters = malloc(sizeof(signal_emitter_t) * total_signal_emitters);
        int signal_emitter_position = 0;
        cJSON_ArrayForEach(signal_emitter_placeholder, signal_emitters_object) {
            cJSON* signal_emitter_id_json = cJSON_GetObjectItemCaseSensitive(signal_emitter_placeholder, "id");
            char* signal_emitter_id = malloc(sizeof(char) * (strlen(signal_emitter_id_json->valuestring) + 1)); //account for \0
            strcpy(signal_emitter_id, signal_emitter_id_json->valuestring);
            signal_emitter_t signal_emitter;
            signal_emitter.id = signal_emitter_id;

            cJSON* signal_json = cJSON_GetObjectItemCaseSensitive(signal_emitter_placeholder, "signal");
            cJSON* signal_base_power_json = cJSON_GetObjectItemCaseSensitive(signal_json, "MAX_POWER");
            signal_t signal = {
                    .base_power = atoi(signal_base_power_json->valuestring)
            };
            signal_emitter.signal = signal;
            signal_emitters[signal_emitter_position] = signal_emitter;
            signal_emitter_position++;
        }
    }
    cJSON_Delete(signal_emitters_object);
    container_t signal_emitters_container = {
            .first = signal_emitters,
            .size = total_signal_emitters,
    };
    return signal_emitters_container;
}

void free_signal_emitters(signal_emitter_t* first, int size) {
    int i = 0;
    for (; i< size ; i++) {
        signal_emitter_t* signal_emitter = first + i;
        free(signal_emitter->id);
    }
    free(first);
}

signal_emitter_t* get_signal_emitter_with_id(char* id, container_t* signal_emitters_container) {
    int i = 0;
    for(; i < signal_emitters_container->size; i++) {
        signal_emitter_t* signal_emitter = (signal_emitter_t*)signal_emitters_container->first + i;
        if(!strcmp(signal_emitter->id, id)) {
            return signal_emitter;
        }
    }
    return NULL;
}

void populate_positions(container_t* anchors_container, container_t* signal_emitters_container) {
    int i = 0;
    for(; i < anchors_container->size; i++) {
        anchor_t* anchor = (anchor_t*)anchors_container->first + i;
        float x = anchor->x;
        float y = anchor->y;
        container_t signal_emitter_ids = anchor->signal_emitter_ids;
        int j = 0;
        for(;j<signal_emitter_ids.size; j++) {
            char* signal_emitter_id = *((char**)signal_emitter_ids.first + j);
            signal_emitter_t* signal_emitter = get_signal_emitter_with_id(signal_emitter_id, signal_emitters_container);
            if(signal_emitter) {
                signal_emitter->x = x;
                signal_emitter->y = y;
            }
        }
    }
}

float compute_coefficient(signal_emitter_t* signal_emitter, float x, float y, int measured_power) {
    float x_diff = x - signal_emitter->x;
    float y_diff = y - signal_emitter->y;
    int base_power = signal_emitter->signal.base_power;
    float real_distance = sqrt((x_diff * x_diff) + (y_diff * y_diff));

    return ((base_power - measured_power)/(10*log10(real_distance)));

}

