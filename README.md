# Bitiato

Bitiato is a binary system for interpreting concepts in a selected language layer, even on
small hardware. Its five primary layers share the same binary positions.
A position's meaning depends on the active layer and convention version.

Bitiato aims for simplicity as a shared benefit for people and machines.
Simpler notation saves resources and makes meaning faster to understand
on both sides.

## Explore the 16 cells

Open [the visual explorer](web/index.html) directly in a browser. It runs
offline without a server or compiler. Choose a language layer first. The
explorer starts at position `0000`, the first equivalence in each layer
of `demo-v1`. Select another layer to interpret the same bits there.

Choose **Follow the concept** to compare conventions. In Vision, red
moves from `0000` in `demo-v1` to `1001` in the illustrative alternate map.
Use **Keep the bits** to stay in the same cell instead.

The explorer reproduces the reference map in the browser. Its alternate
map is for illustration and is independent of the C99 demo.

## Explore the Level 2 UI language

Open the [UI Symbol Lab](web/ui/index.html) to compose basic UI components
with reusable properties and states. The [UI language notes](docs/ui-language.md)
describe the notation, the symbol font and how to rebuild it.

## Run the five senses demo

From the repository root, build with a C99 compiler on macOS or Linux.
The demo uses the C standard library and its map is compiled into the
executable, so it also runs offline.

```sh
cc -std=c99 -Wall -Wextra -pedantic -Werror \
  src/bitiato.c conventions/demo_v1.c src/demo.c -o bitiato-demo
./bitiato-demo vision
```

On Windows with GCC (for example, from MinGW-w64), run these commands from
PowerShell.

```powershell
gcc -std=c99 -Wall -Wextra -pedantic -Werror src/bitiato.c conventions/demo_v1.c src/demo.c -o bitiato-demo.exe
.\bitiato-demo.exe vision
```

The first argument selects the language layer. The position defaults to
`0000`. Run `./bitiato-demo all` to compare the five interpretations. The columns are convention, layer, input bits, concept ID
and label.

```text
demo-v1 | Vision | 0000 | 1 | red
demo-v1 | Hearing | 0000 | 5 | do
demo-v1 | Smell | 0000 | 9 | floral
demo-v1 | Taste | 0000 | 13 | sweet
demo-v1 | Touch | 0000 | 17 | soft
```

Pass four bits after the layer key to try another position. In PowerShell, use `.\bitiato-demo.exe` with the same arguments.

| Invocation | Result |
| --- | --- |
| `./bitiato-demo hearing 0011` | `demo-v1 \| Hearing \| 0011 \| 8 \| fa` |
| `./bitiato-demo touch 0011` | `demo-v1 \| Touch \| 0011 \| 20 \| hot` |
| `./bitiato-demo vision 0100` | `demo-v1 \| Vision \| 0100 \| 0 \| unassigned` |
| `./bitiato-demo touch 1111` | `demo-v1 \| Touch \| 1111 \| 0 \| unassigned` |
| `./bitiato-demo vision 10000` | Usage on standard error, exit status 2 |
| `./bitiato-demo ui 0000` | Usage on standard error, exit status 2 |

The full map is in the [architecture notes](docs/architecture.md).
The labels are experimental assignments. The demo returns concept IDs
and labels without generating physical stimuli.

## Run the tests

```sh
cc -std=c99 -Wall -Wextra -pedantic -Werror \
  src/bitiato.c conventions/demo_v1.c tests/test_bitiato.c -o bitiato-test
./bitiato-test
```

```powershell
gcc -std=c99 -Wall -Wextra -pedantic -Werror src/bitiato.c conventions/demo_v1.c tests/test_bitiato.c -o bitiato-test.exe
.\bitiato-test.exe
```

The tests cover all 80 layer and position pairs, the 20 assignments, the 60
unassigned entries, invalid inputs and the use of an alternate local map.

## Repository layout

- `src/` contains the C99 interpreter and the separate terminal demo.
- `conventions/` contains the versioned demo map and its labels.
- `tests/` contains the executable reference tests.
- `docs/` contains architectural decisions and open questions.
- `web/` contains the offline visual explorer.

The [architecture notes](docs/architecture.md) cover compatibility,
offline operation, composition and potential microcontroller targets.

## License

Bitiato is available under the [MIT License](LICENSE).
