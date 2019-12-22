#include <esp_tls.h>
#include "http.h"
#include "esp_http_client.h"
#include "esp_log.h"
#include "config.h"

#define TAG "HTTP"


esp_err_t _http_event_handler(esp_http_client_event_t *evt)
{
    switch(evt->event_id) {
        case HTTP_EVENT_ERROR:
            ESP_LOGD(TAG, "HTTP_EVENT_ERROR");
            break;
        case HTTP_EVENT_ON_CONNECTED:
            ESP_LOGD(TAG, "HTTP_EVENT_ON_CONNECTED");
            break;
        case HTTP_EVENT_HEADER_SENT:
            ESP_LOGD(TAG, "HTTP_EVENT_HEADER_SENT");
            break;
        case HTTP_EVENT_ON_HEADER:
            ESP_LOGD(TAG, "HTTP_EVENT_ON_HEADER, key=%s, value=%s", evt->header_key, evt->header_value);
            break;
        case HTTP_EVENT_ON_DATA:
            ESP_LOGD(TAG, "HTTP_EVENT_ON_DATA, len=%d", evt->data_len);
            if (!esp_http_client_is_chunked_response(evt->client)) {
                response_collector_t* response_collector = evt->user_data;
                if(!response_collector->data) {
                    //first time,create buffer
                    int content_length = esp_http_client_get_content_length(evt->client);
                    char* buffer = malloc(content_length + 1);
                    buffer[content_length] = '\0';
                    response_collector->data = buffer;
                }
                memcpy(response_collector->data + response_collector->next_location, evt->data, evt->data_len);
                response_collector->next_location += evt->data_len;
            }
            break;
        case HTTP_EVENT_ON_FINISH:
            ESP_LOGD(TAG, "HTTP_EVENT_ON_FINISH");
            break;
        case HTTP_EVENT_DISCONNECTED:
            ESP_LOGD(TAG, "HTTP_EVENT_DISCONNECTED");
            int mbedtls_err = 0;
            esp_err_t err = esp_tls_get_and_clear_last_error(evt->data, &mbedtls_err, NULL);
            if (err != 0) {
                ESP_LOGD(TAG, "Last esp error code: 0x%x", err);
                ESP_LOGD(TAG, "Last mbedtls failure: 0x%x", mbedtls_err);
            }
            break;
    }
    return ESP_OK;
}

esp_http_client_config_t _get_base_client_config() {
    esp_http_client_config_t config = {
            .host = HTTP_HOST,
            .port = HTTP_PORT,
            .user_data = NULL,
            .event_handler = _http_event_handler,
    };

    return config;
}

esp_http_client_handle_t _get_client(
        char* path,
        esp_http_client_method_t method,
        response_collector_t* response_collector) {

    esp_http_client_config_t config = _get_base_client_config();

    config.user_data = response_collector;
    config.path = path;
    config.method = method;

    return esp_http_client_init(&config);
}

http_response_t _perform(
        esp_http_client_handle_t client,
        response_collector_t* response_collector) {

    esp_err_t err = esp_http_client_perform(client);

    http_response_t response = {
            .code = 500,
            .length = 0,
            .data = NULL
    };

    if (err == ESP_OK) {
        int status_code = esp_http_client_get_status_code(client);
        int content_length = esp_http_client_get_content_length(client);
        ESP_LOGD(TAG, "HTTP Status = %d, content_length = %d",
                 status_code,
                 content_length);
        char* buffer = response_collector->data;
        response.code = status_code;
        response.length = content_length;
        response.data = buffer;
    } else {
        ESP_LOGE(TAG, "HTTP request failed: %s",  esp_err_to_name(err));
    }

    esp_http_client_cleanup(client);
    return response;
}

http_response_t get(char* path) {
    response_collector_t rp = {
            .next_location = 0,
            .data = NULL
    };
    esp_http_client_handle_t client = _get_client(path, HTTP_METHOD_GET, &rp);
    return _perform(client, &rp);
}

http_response_t put(char* path, char* body, int len) {
    response_collector_t rp = {
            .next_location = 0,
            .data = NULL
    };
    esp_http_client_handle_t client = _get_client(path, HTTP_METHOD_PUT, &rp);
    esp_http_client_set_header(client, CONTENT_TYPE_HEADER, APPLICATION_JSON);
    esp_http_client_set_post_field(client, body, len);
    return _perform(client, &rp);
}

http_response_t post(char* path, char* body, int len) {
    response_collector_t rp = {
            .next_location = 0,
            .data = NULL
    };
    esp_http_client_handle_t client = _get_client(path, HTTP_METHOD_POST, &rp);
    esp_http_client_set_header(client, CONTENT_TYPE_HEADER, APPLICATION_JSON);
    esp_http_client_set_post_field(client, body, len);
    return _perform(client, &rp);
}

void free_response(http_response_t* response) {
    free(response->data);
}