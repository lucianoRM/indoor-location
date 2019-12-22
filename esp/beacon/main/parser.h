#ifndef BEACON_PARSER_H
#define BEACON_PARSER_H

#include "list.h"

typedef struct signal {
    int base_power; //The base power configured by the server
    float coeff; //The medium coefficient computed
    float power_average; //The power average measured my this beacon
} signal_t;

typedef struct signal_emitter {
    char* id;
    float x;
    float y;
    signal_t* signal;
} signal_emitter_t;

typedef struct anchor {
    char* id;
    float x;
    float y;
    llist* signal_emitter_ids;
} anchor_t;

/**
 * Take a json string and return a container with all the anchors parsed
 * @param json_string
 * @return
 */
llist* parse_anchors(char* json_string);

/**
 * Free dynamic memory of all anchors in the array
 */
void free_anchors(llist* anchors_list);

/**
 * Take a json string and return a container with all the signal emitters parsed
 * @param json_string
 * @return
 */
llist* parse_signal_emitters(char* json_string);

/**
 * Free dynamically allocated memory of all signal emitters
 */
void free_signal_emitters(llist* signal_emitters_list);

/**
 * Build json to send to server with the signal data
 * @param signal
 * @return
 */
char* build_signal_json(signal_t* signal);

#endif //BEACON_PARSER_H
