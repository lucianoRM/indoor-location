#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"
#include "location_system.h"

int main() {
    char* signal_emitters_response = "[\n"
                                          "    {\n"
                                          "        \"name\": null,\n"
                                          "        \"signal\": {\n"
                                          "            \"MAX_POWER\": \"-60\",\n"
                                          "            \"MEDIUM_COEF\":\"2.5\"\n"
                                          "        },\n"
                                          "        \"id\": \"1\"\n"
                                          "    },\n"
                                          "    {\n"
                                          "        \"name\": null,\n"
                                          "        \"signal\": {\n"
                                          "            \"MAX_POWER\": \"-60\",\n"
                                          "            \"MEDIUM_COEF\":\"2.5\"\n"
                                          "        },\n"
                                          "        \"id\": \"2\"\n"
                                          "    }\n"
                                          "]";
    char* anchors_response = "[\n"
                             "    {\n"
                             "        \"sensors\": {},\n"
                             "        \"signal_emitters\": {\n"
                             "            \"1\": {\n"
                             "                \"name\": null,\n"
                             "                \"signal\": {\n"
                             "                    \"MAX_POWER\": \"-60\",\n"
                             "                    \"MEDIUM_COEF\":\"2.5\"\n"
                             "                },\n"
                             "                \"id\": \"1\"\n"
                             "            }\n"
                             "        },\n"
                             "        \"name\": null,\n"
                             "        \"position\": {\n"
                             "            \"x\": 0.0,\n"
                             "            \"y\": 0.0\n"
                             "        },\n"
                             "        \"id\": \"a1\"\n"
                             "    },\n"
                             "    {\n"
                             "        \"sensors\": {},\n"
                             "        \"signal_emitters\": {\n"
                             "            \"2\": {\n"
                             "                \"name\": null,\n"
                             "                \"signal\": {\n"
                             "                    \"MAX_POWER\": \"-60\",\n"
                             "                    \"MEDIUM_COEF\":\"2.5\"\n"
                             "                },\n"
                             "                \"id\": \"2\"\n"
                             "            }\n"
                             "        },\n"
                             "        \"name\": null,\n"
                             "        \"position\": {\n"
                             "            \"x\": 7.0,\n"
                             "            \"y\": 3.0\n"
                             "        },\n"
                             "        \"id\": \"a2\"\n"
                             "    }\n"
                             "]";

    container_t anchors = parse_anchors(anchors_response);
    int i;
//    for(i = 0; i < anchors.size; i++) {
//        anchor_t anchor = *((anchor_t*)anchors.first + i);
//        printf("ID: %s\n", anchor.id);
//        printf("X: %f, Y: %f\n", anchor.x, anchor.y);
//        printf("SEs\n");
//        container_t signal_emitters = anchor.signal_emitter_ids;
//        int j;
//        for(j = 0; j < signal_emitters.size; j++) {
//            char* signal_emitter_id = *((char**)signal_emitters.first + j);
//            printf("se: %s\n", signal_emitter_id);
//        }
//    }
//


    container_t signal_emitters = parse_signal_emitters(signal_emitters_response);

    populate_positions(&anchors, &signal_emitters);

    for(i = 0; i < signal_emitters.size; i++) {
        signal_emitter_t signal_emitter = *((signal_emitter_t*)signal_emitters.first + i);
        printf("se id: %s\n", signal_emitter.id);
        printf("x: %f, y: %f\n\n", signal_emitter.x, signal_emitter.y);
        printf("signal: %d\n", signal_emitter.signal.base_power);
        printf("coeff: %f\n", compute_coefficient(&signal_emitter, 0.0f, 0.0f, -104));
    }


    free_anchors(anchors.first, anchors.size);
    free_signal_emitters(signal_emitters.first, signal_emitters.size);

    return 0;
}