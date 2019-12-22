#include <stdio.h>
#include "list.h"

int main() {
    list* list;
    list_insert(list, (void*)1);
    list_insert(list, (void*)2);
    list_insert(list, (void*)3);
    void* a;
    FOREACH(a, list) {
        printf("element: %d", (int)a);
    }

    printf("list size: %d", list_size(list));
    list_destroy(list);
}