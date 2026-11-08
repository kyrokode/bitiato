# Level 2 UI language

The UI language builds on the primary language layers. A component has a
conceptual identity that could be expressed through several senses. This
prototype provides visual notation. Cross-sensory equivalences still
need to be defined and validated for each concept.

## Basic components

The [component catalog](../web/ui/components.json) assigns one pictogram
and one code point to each of these initial components.

| Group | Components |
| --- | --- |
| Controls | Button, Checkbox, Radio Button, Switch, Select, Slider |
| Input | Text Field, Text Area |
| Content | Text, Label, Image, Icon, Heading |
| Navigation | Link, Menu, Menu Item, Tab |
| Structure | List, List Item, Dialog, Container, Divider, Table |
| Feedback | Progress Bar, Alert |

Choose a component in the lab, then add it to the sequence. Each
component has its own properties and state. The composer represents
their declarations. It does not render them as working controls.

## Initial property inventory

Bitiato UI uses dedicated glyphs for components, properties, and states.
The [catalog](../web/ui/symbols.json) defines the code point, family, kind,
and draft compatibility of each entry. The families organize
the catalog and have no separate tokens. Property glyphs use pictograms to suggest their meaning. Name is a tag,
Parent points to an upper node, Editable is a pencil, and Duration spans
two endpoints. The labels in the lab explain the pictograms while their
interpretation is being refined.

| Order | Group | Family | Fundamental question | Initial symbols |
| --- | --- | --- | --- | --- |
| 01 | Definition | Identity | What is it? | ID, Name, Type |
| 02 | Definition | Structure | How is it organized? | Parent, Children, Order |
| 03 | Definition | Relationships | What does it relate to? | Belongs to, Controls, References |
| 04 | Information | Data | What information does it hold or receive? | Source, Destination, Data reference |
| 05 | Information | Content | What does it contain or express? | Text, Value, Items |
| 06 | Information | Accessibility | How can it be recognized and interpreted? | Accessible name, Description, Role |
| 07 | Possibilities | Capabilities | What can it do? | Editable, Selectable, Expandable |
| 08 | Possibilities | Constraints | What are its limits? | Minimum, Maximum, Required |
| 09 | Possibilities | Validation | What conditions must it satisfy? | Value type, Format, Pattern |
| 10 | Condition | States | What condition is it in? | Focused, Pressed, Disabled, Active, Selected |
| 11 | Interaction | Events | What happens? | Press event, Change event, Input event |
| 12 | Interaction | Behavior | How does it respond? | Toggle, Submit, Navigate, Action |
| 13 | Interaction | Temporality | When and for how long? | Duration, Interval, Delay |

Accessibility applies across all groups and sensory layers. Its place in
the catalog expresses how a concept is recognized. It carries no
execution order. Temporality remains independent of states, events,
and behavior.

Type identifies a component classification. Value type constrains its
data. References describes a component relationship. Data reference
identifies a datum. Pressed is a state. Press event names an occurrence
to which a handler can be bound. Action binds a general operation.
These distinctions keep the inventory independent of a UI framework.

The [symbol lab](../web/ui/index.html) displays the compatibility matrix
for Button, List, Menu, Text Field, and List Item. The remaining
components have no compatibility entries yet. The lab offers every
symbol for exploration.
Color, elevation, iconography, visual motion, shape, spacing, and
typography belong to the representation. Timing remains a separate
concept that may later qualify a particular operation or transition.

## Composition rule

Start with a component glyph. Append property glyphs and, optionally,
one state glyph. A property can appear once per component.

| Boundary | Spaces |
| --- | --- |
| Between symbols in the same family | None |
| Component to its first family | Two |
| Between families of the same component | Two |
| Property to its optional value | Two |
| Between components | Three |

Separators start at two spaces because common text never uses two
consecutive spaces. A single space always belongs to a value. After a
value, the next symbol is preceded by two spaces even within the same
family. Write a value directly after its two spaces. The composer adds no quotation
marks or other wrappers. A value may contain single spaces, as in
`Save draft`. The composer trims outer whitespace and rejects repeated
spaces, other whitespace, and private-use symbols in values so boundaries
stay distinguishable. State glyphs are standalone.

Choose a family and then a symbol. States use the same controls as other
families. Adding a state replaces the previous state. Add another component
to see the three-space boundary between components.

The lab serializes selections in canonical family order. The notation
allows compatible symbols to be written in other orders when they are
independent. The families are a working classification. Whether entries
such as validation rules can be expressed through simpler concepts
remains open.

The font uses Unicode Private Use Area code points under Bitiato's
local convention. Readers need the same symbol map and font for the
intended glyphs. The binary encoding of UI symbols remains open.
See the [Unicode FAQ](https://www.unicode.org/faq/private_use.html) and
[WAI-ARIA's state and property model](https://www.w3.org/TR/wai-aria/#states_and_properties)
for background.

## Try and rebuild

Open the [symbol lab](../web/ui/index.html) to inspect and compose symbols.
The [TrueType font](../web/ui/bitiato_ui.ttf) can also be installed in a
desktop font manager. Rebuild the font and browser catalog together
after editing the inventory or outlines.

```sh
python3 -m pip install fonttools==4.60.1
python3 web/ui/build_font.py
```
