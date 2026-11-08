#include "bitiato.h"

int bitiato_interpret(const struct bitiato_map *map, unsigned int layer,
                      unsigned int position)
{
    if (!map || layer >= BITIATO_LAYER_COUNT ||
        position >= BITIATO_POSITION_COUNT) {
        return BITIATO_INVALID;
    }

    return map->ids[layer][position];
}
