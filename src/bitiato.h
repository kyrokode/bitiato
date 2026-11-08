#ifndef BITIATO_H
#define BITIATO_H

#include <stdint.h>

enum bitiato_layer {
    BITIATO_VISION,
    BITIATO_HEARING,
    BITIATO_SMELL,
    BITIATO_TASTE,
    BITIATO_TOUCH,
    BITIATO_LAYER_COUNT
};

enum {
    BITIATO_POSITION_COUNT = 16,
    BITIATO_UNASSIGNED = 0,
    BITIATO_INVALID = -1
};

struct bitiato_map {
    uint8_t ids[BITIATO_LAYER_COUNT][BITIATO_POSITION_COUNT];
};

/* Returns an ID, BITIATO_UNASSIGNED or BITIATO_INVALID. */
int bitiato_interpret(const struct bitiato_map *map, unsigned int layer,
                      unsigned int position);

#endif
