#ifndef BLINK_LIST_H
#define BLINK_LIST_H

#include <sys/queue.h>

#define __INDEX__ __i__
#define __CONCAT2__(x,y) x##y
#define __CONCAT__(x,y) __CONCAT2__(x,y)
#define	__FOREACH__(var, index, list) int (index) = 0; for((var) = llist_get(list, (index)); (list) && (index)++ < (list)->size ; (var) = llist_get(list, (index)))

#define	FOREACH(var, list) __FOREACH__((var), __CONCAT__(__INDEX__, __LINE__), (list))

/**
 * Node in the linked list
 */
typedef struct node {
    void* value;
    SLIST_ENTRY(node) next;
} _node;

/**
 * Linked list struct
 */
typedef struct llist {
    int size;
    SLIST_HEAD(_head,node) head;
} llist;

/**
 * Creates a new empty list allocating memory for it
 * @return a pointer to the created list.
 */
llist* llist_create();

/**
 * Destroys the list removing all elements and freeing allocated memory.
 * If the list is not empty, the pointers to the data allocated will be lost, so users should first release that memory.
 */
void llist_destroy(llist* list);

/**
 * Insert a new element in the list
 * @param list
 * @param element
 */
void llist_insert(llist* list, void* element);

/**
 * Remove the element in the given position from the list and return that element.
 * Internal memory will be released but it's up to the user to free memory used by the element itself
 * @param list
 * @param position
 * @return the element removed.
 */
void* llist_remove(llist* list, int position);

/**
 * @param list
 * @param position
 * @return the element from the position given
 */
void* llist_get(llist* list, int position);

/**
 * @param list
 * @return the size of the list
 */
int llist_size(llist* list);



#endif //BLINK_LIST_H
