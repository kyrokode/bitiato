# Bitiato architecture

Bitiato starts with binary values `0` and `1`. Its primary human language layers are
**Vision, Hearing, Smell, Taste and Touch**. All five are peers and reuse the
same logical positions with equal capacity. Switching the active layer
changes the meaning of the same bits. Equal capacity describes the code
space. Each sense can have different physical and informational properties.

Bitiato is the primary system. The nine types of intelligence and UI
components belong to later levels as concepts or compositions. Concepts,
properties and states are intended to be autonomous and concatenable
under one grammar organised by levels. The grammar and the rules for
composition are pending. A future UI can consume Bitiato independently
of React or any other framework. The current terminal demo is a caller of
the core.

## Reference convention `demo-v1`

Each layer has 16 logical positions, represented by `0000` through `1111`.
Choose the language layer first. Position `0000` holds its first
illustrative equivalence. The table lists every position. The final range covers all twelve unassigned
positions in each layer. Parentheses contain the demo's local concept IDs.

| Position | Vision | Hearing | Smell | Taste | Touch |
| --- | --- | --- | --- | --- | --- |
| `0000` | red (1) | do (5) | floral (9) | sweet (13) | soft (17) |
| `0001` | green (2) | re (6) | citrus (10) | salty (14) | rough (18) |
| `0010` | blue (3) | mi (7) | smoky (11) | sour (15) | cold (19) |
| `0011` | white (4) | fa (8) | minty (12) | bitter (16) | hot (20) |
| `0100`–`1111` | unassigned (0) | unassigned (0) | unassigned (0) | unassigned (0) | unassigned (0) |

These assignments are experimental. Sharing a position creates no natural
equivalence between senses. For example, interpreting a code as
`floral` selects a label. Producing a smell would require physical hardware
and a separate specification. A fuller treatment of colour or sound can
later explore composition within Vision or Hearing.

The C99 core takes a local map, a layer and a position. It returns a concept
ID, `0` for an unassigned position or `-1` for invalid input. The caller
supplies the active layer for each lookup, so independent callers can
interpret the same position in different language layers. The position stays
within `0`–`15` even when it has no assignment in the selected map.
Concept IDs are local to the demo convention and are lookup outputs.

The map holds 80 bytes of ID data, one byte per entry. That size excludes
program code, labels, caller state and platform-specific storage overhead.
The core and numeric map use neither dynamic allocation nor I/O. The
terminal demo supplies input, prints labels and reports invalid arguments.

## Versions and offline operation

A convention is defined separately from the interpreter. Each version
specifies a complete map across layers and positions, including unassigned
entries. A new version may assign positions differently. Keep earlier
version definitions available and unchanged so their meanings remain
valid and reproducible.

Each session uses one convention version that both endpoints actually
implement. A device that only implements `v58` can exchange Bitiato data
only in `v58`. A new `v8000` device can also speak `v58` if it ships with
or installs and actually implements that convention. Its arrival has no
effect on the software or map on an older device.

| Example endpoints | Version for the session |
| --- | --- |
| Flipper with `v58` and phone with `v58` and `v8000` | `v58` |
| That phone and server with `v8000` | `v8000` |
| That Flipper and server | No common version |

If a concept such as a button moves between conventions, the phone looks
up the position in the convention for its current session. Wide-area
network access can distribute new conventions. The device continues to
interpret data with its installed convention when offline.

`v58` and `v8000` illustrate interoperability. This repository implements
`demo-v1` and a local lookup. Version identification, agreement on a shared
version and the distribution format remain open.

## Logical positions and signalling

The four bits describe a logical position in the demo. All 16 positions
are available in every layer. The earlier README counted the positions
remaining in a hypothetical stream after reserving some values for layer
selectors. That arithmetic describes one possible transport design.

A fixed-width selector for five layers would need at least three bits
as a standalone field. That bound says nothing about the total cost of
framing, sending a layer change or identifying a version. The wire format,
any reserved values and the final bit cost remain to be designed. The
CLI selects the layer first and then reads the logical position.

## Hardware and other runtimes

A small board can compile the same core and numeric map and supply the
layer and position from its own test inputs. Candidate targets include
an Arduino-compatible board, an ESP32 and a Cortex-M board. A board test
could cycle the layer at fixed position `0000`, report the five expected
IDs over serial, then try `1111` and an out-of-range position. The actual
flash and RAM use should be read from the board build.

The architecture is independent of C. A future WebAssembly build could
reuse the interpreter and provide its own browser adapter. The current browser explorer uses its own display map. Physical board
execution remains a separate verification step.
