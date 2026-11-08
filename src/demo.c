#include <stdio.h>
#include <string.h>

#include "../conventions/demo_v1_labels.h"

static const char *const layer_names[BITIATO_LAYER_COUNT] = {
    "Vision", "Hearing", "Smell", "Taste", "Touch"
};

static const char *const layer_keys[BITIATO_LAYER_COUNT] = {
    "vision", "hearing", "smell", "taste", "touch"
};

static int parse_position(const char *bits)
{
    int position = 0;

    if (strlen(bits) != 4) {
        return BITIATO_INVALID;
    }
    for (; *bits; ++bits) {
        if (*bits != '0' && *bits != '1') {
            return BITIATO_INVALID;
        }
        position = position * 2 + (*bits - '0');
    }
    return position;
}

int main(int argc, char *argv[])
{
    const char *key = argc > 1 ? argv[1] : "";
    const char *bits = argc > 2 ? argv[2] : "0000";
    int position = parse_position(bits);
    unsigned int first_layer = 0;
    unsigned int end_layer = BITIATO_LAYER_COUNT;

    if (strcmp(key, "all") != 0) {
        while (first_layer < BITIATO_LAYER_COUNT &&
               strcmp(key, layer_keys[first_layer]) != 0) {
            ++first_layer;
        }
        end_layer = first_layer + 1;
    }
    if (argc > 3 || position == BITIATO_INVALID ||
        first_layer >= BITIATO_LAYER_COUNT) {
        fprintf(stderr, "Usage: %s {vision|hearing|smell|taste|touch|all} [BBBB]\n",
                argv[0]);
        return 2;
    }
    for (unsigned int layer = first_layer; layer < end_layer; ++layer) {
        int id = bitiato_interpret(&bitiato_demo_v1_map, layer,
                                   (unsigned int)position);
        printf("%s | %s | %s | %d | %s\n", BITIATO_DEMO_V1,
               layer_names[layer], bits, id, bitiato_demo_v1_labels[id]);
    }
    return 0;
}
