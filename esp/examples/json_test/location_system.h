#ifndef location_system__h
#define location_system__h

//Real simple way of returning the size of an array
typedef struct container {
    void* first;
    int size;
} container_t;

typedef struct signal {
    int base_power;
} signal_t;

typedef struct signal_emitter {
    char* id;
    float x;
    float y;
    signal_t signal;
} signal_emitter_t;

typedef struct anchor {
    char* id;
    float x;
    float y;
    container_t signal_emitter_ids;
} anchor_t;

/**
 * Take a json string and return a container with all the anchors parsed
 * @param json_string
 * @return
 */
container_t parse_anchors(char* json_string);

/**
 * Free dynamic memory of all anchors in the array
 * @param first
 * @param size
 */
void free_anchors(anchor_t* first, int size);

/**
 * Take a json string and return a container with all the signal emitters parsed
 * @param json_string
 * @return
 */
container_t parse_signal_emitters(char* json_string);

/**
 * Free dynamically allocated memory of all signal emitters
 * @param first
 * @param size
 */
void free_signal_emitters(signal_emitter_t* first, int size);

/**
 * Use the information from the anchors to populate the positions of the signal emitters
 * @param anchors_container
 * @param signal_emitters_container
 */
void populate_positions(container_t* anchors_container, container_t* signal_emitters_container);

/**
 * Given the current measurements, compute the medium coefficient
 * @param signal_emitter
 * @param x
 * @param y
 * @param measured_power
 * @return
 */
float compute_coefficient(signal_emitter_t* signal_emitter, float x, float y, int measured_power);



#endif