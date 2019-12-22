#include <stdlib.h>
#include "list.h"
#include <sys/queue.h>

list* list_create() {
    list* listptr = malloc(sizeof(list));
    SLIST_INIT(&(listptr->head));
    listptr->size = 0;
    return listptr;
}

void list_destroy(list* list) {
    if(!list) return;

    int size = list_size(list);
    for (int i = 0; i < size; i++) {
        list_remove(list, 0);
    }
    free(list);
}

void list_insert(list* list, void* element) {
    if(!list) return;
    _node* entry = malloc(sizeof(_node));
    entry->value = element;
    SLIST_INSERT_HEAD(&list->head, entry, next);
    list->size++;
}

void* list_remove(list* list, int position) {
    if (!list) return NULL;

    int i = 0;
    _node* tmp_node;
    _node* node_to_remove = NULL;
    SLIST_FOREACH(tmp_node, &list->head, next) {
        if (i == position) {
            node_to_remove = tmp_node;
        }
        i++;
    }
    if (node_to_remove) {
        SLIST_REMOVE(&list->head, node_to_remove, node, next);
        void* value = node_to_remove->value;
        free(node_to_remove);
        list->size--;
        return value;
    }
    return NULL;
}

void* list_get(list* list, int position) {
    if (!list) return NULL;

    int i = 0;
    _node* tmp_node;
    _node* node_to_return = NULL;
    SLIST_FOREACH(tmp_node, &list->head, next) {
        if (i == position) {
            node_to_return = tmp_node;
        }
        i++;
    }
    if (node_to_return) {
        return node_to_return->value;
    }
    return NULL;
}

int list_size(list* list) {
    if(!list) return 0;

    return list->size;
}