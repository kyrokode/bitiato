# Bitiato

A shared binary language, even for simple hardware.

Bitiato is an open-source project for encoding concepts in a small binary
code space. Devices interpret each position using an active layer and a
shared version of the convention.

## Architecture

- **Layers reuse positions.** The same binary position can identify a letter,
  a musical note, or a color in different layers. The meaning depends on the
  convention version, the active layer, and the position.
- **Every version defines a complete convention.** It defines all its layers
  and the positions assigned to their concepts. A new version may rearrange
  those assignments. Published versions keep their original mappings and
  remain usable.
- **Devices use a shared convention for each exchange.** A device may support
  one version or several. Compatibility is specific to the two endpoints and
  the version they use for that exchange.
- **Distribution and operation are separate.** Conventions are defined
  externally and can be distributed over a wide-area network (WAN). Connected
  devices can adopt newer versions. Offline devices continue using their
  installed convention.

## A four-bit example

Four bits offer 16 code values. An illustrative convention could reserve two
values to select a layer and reuse the other 14 positions in each layer.
That gives 28 possible concept assignments across two layers. Reserving four
selectors instead leaves 12 positions per layer, or 48 assignments across
four layers. These totals count assignments across contexts. Selecting the
context also consumes a code value when it is sent.

## Interoperability example

Suppose a Flipper is built with convention `v58`, a phone supports both
`v58` and `v8000`, and a server supports only `v8000`.

| Devices | Convention for the exchange |
| --- | --- |
| Flipper and phone | `v58` |
| Phone and server | `v8000` |
| Flipper and server | No shared version |

If the same button occupies different positions in `v58` and `v8000`, the
phone uses the `v58` position when it talks to the Flipper.

## Project status

This README records the initial design. The wire format and the mechanism
for selecting a shared version are open design questions.

## License

Bitiato is available under the [MIT License](LICENSE).
