#ifndef BEACON_HTTP_H
#define BEACON_HTTP_H

#define CONTENT_TYPE_HEADER "Content-Type"
#define APPLICATION_JSON "application/json"

typedef struct response_collector {
    char* data;
    int next_location;
} response_collector_t;

typedef struct response {
    int code;
    int length;
    char* data;
} http_response_t;

/**
 * GET from path
 * @param path
 * @return
 */
http_response_t get(char* path);

/**
 * PUT on path
 * @param put
 * @param body
 * @param len
 * @return
 */
http_response_t put(char* put, char* body, int len);

/**
 * POST on path
 * @param put
 * @param body
 * @param len
 * @return
 */
http_response_t post(char* put, char* body, int len);

/**
 * Clear memory used for response
 * @param response
 */
void free_response(http_response_t* response);

#endif //BEACON_HTTP_H
