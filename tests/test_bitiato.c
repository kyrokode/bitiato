#include <assert.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>

#include "../conventions/demo_v1_labels.h"

int main(void)
{
    const int expected[5][4] = {
        {1, 2, 3, 4}, {5, 6, 7, 8}, {9, 10, 11, 12},
        {13, 14, 15, 16}, {17, 18, 19, 20}
    };

    const char *const labels[5][4] = {
        {"red", "green", "blue", "white"},
        {"do", "re", "mi", "fa"},
        {"floral", "citrus", "smoky", "minty"},
        {"sweet", "salty", "sour", "bitter"},
        {"soft", "rough", "cold", "hot"}
    };

    assert(BITIATO_LAYER_COUNT == 5);
    assert(BITIATO_POSITION_COUNT == 16);
    assert(sizeof bitiato_demo_v1_map.ids == 80);

    /* Hold the position fixed while switching through all five layers. */
    for (unsigned int position = 0; position < 16; ++position) {
        for (unsigned int layer = 0; layer < 5; ++layer) {
            int id = bitiato_interpret(&bitiato_demo_v1_map, layer, position);
            assert(id == (position < 4 ? expected[layer][position] : 0));
            assert((unsigned int)id < sizeof bitiato_demo_v1_labels /
                                      sizeof bitiato_demo_v1_labels[0]);
            assert(strcmp(bitiato_demo_v1_labels[id],
                          position < 4 ? labels[layer][position] :
                                         "unassigned") == 0);
        }
        assert(bitiato_interpret(&bitiato_demo_v1_map, 5, position) ==
               BITIATO_INVALID);
    }
    for (unsigned int layer = 0; layer < 5; ++layer) {
        assert(bitiato_interpret(&bitiato_demo_v1_map, layer, 16) ==
               BITIATO_INVALID);
        assert(bitiato_interpret(&bitiato_demo_v1_map, layer, UINT_MAX) ==
               BITIATO_INVALID);
    }
    assert(bitiato_interpret(&bitiato_demo_v1_map, UINT_MAX, 0) ==
           BITIATO_INVALID);
    assert(bitiato_interpret(NULL, 0, 0) == BITIATO_INVALID);

    /* All four bits remain available even with a different map. */
    const struct bitiato_map another_map = {{
        [BITIATO_TOUCH] = {[15] = 255}
    }};
    assert(bitiato_interpret(&another_map, BITIATO_TOUCH, 15) == 255);
    assert(bitiato_interpret(&bitiato_demo_v1_map, BITIATO_TOUCH, 15) ==
           BITIATO_UNASSIGNED);

    puts("OK: 80 layer and position pairs, bounds, and an alternate map.");
    return 0;
}
