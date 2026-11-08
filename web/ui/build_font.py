"""Build the Bitiato UI symbol font with FontTools."""

import json
from math import hypot
from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables._g_l_y_f import flagOverlapSimple


def polygon(pen, points):
    pen.moveTo(points[0])
    for point in points[1:]:
        pen.lineTo(point)
    pen.closePath()


def rectangle(pen, left, bottom, right, top):
    points = [(left, bottom), (left, top), (right, top), (right, bottom)]
    polygon(pen, points)


def button(pen):
    polygon(pen, [(80, 220), (80, 540), (140, 600), (760, 600),
                  (820, 540), (820, 220), (760, 160), (140, 160)])
    polygon(pen, [(155, 255), (175, 235), (725, 235), (745, 255),
                  (745, 505), (725, 525), (175, 525), (155, 505)])
    rectangle(pen, 320, 345, 580, 415)


def focused(pen):
    corner = [(90, 430), (165, 430), (165, 525),
              (230, 525), (230, 600), (90, 600)]
    for mirror_x in (False, True):
        for mirror_y in (False, True):
            points = [(520 - x if mirror_x else x, 760 - y if mirror_y else y)
                      for x, y in corner]
            polygon(pen, points[::-1] if mirror_x != mirror_y else points)


def pressed(pen):
    polygon(pen, [(222, 605), (222, 415), (116, 415), (260, 272),
                  (404, 415), (298, 415), (298, 605)])
    rectangle(pen, 105, 155, 415, 224)


def disabled(pen):
    polygon(pen, [(109, 220), (260, 371), (411, 220), (464, 273),
                  (313, 424), (464, 575), (411, 628), (260, 477),
                  (109, 628), (56, 575), (207, 424), (56, 273)])


def active(pen):
    polygon(pen, [(260, 610), (440, 380), (260, 150), (80, 380)])


def selected(pen):
    polygon(pen, [(70, 370), (130, 430), (225, 335), (405, 515),
                  (465, 455), (225, 215)])


# Paths use a 24-unit grid with coordinates measured from the top left.
PROPERTY_OUTLINES = {
    # ID
    0xE200: "3,8 3,4 21,4 21,20 3,20 3,8 | 8,9 | 6,15 8,13 10,15 | 13,9 18,9 | 13,14 18,14",
    # Name
    0xE201: "3,12 10,5 21,5 21,19 10,19 3,12 | 10,12 | 14,10 18,10 | 14,14 18,14",
    # Type
    0xE202: "4,10 7,4 10,10 4,10 | 14,4 20,4 20,10 14,10 14,4 | 12,14 16,18 12,22 8,18 12,14",
    # Parent
    0xE220: "9,3 15,3 15,8 9,8 9,3 | 12,8 12,19 | 8,15 12,11 16,15",
    # Children
    0xE221: "12,4 | 12,7 12,11 | 5,16 5,11 19,11 19,16 | 5,20 | 19,20",
    # Order
    0xE222: "7,5 20,5 | 7,12 16,12 | 7,19 12,19 | 3,5 | 3,12 | 3,19",
    # Belongs to
    0xE230: "9,4 20,4 20,20 9,20 9,16 | 9,4 9,8 | 3,12 14,12 | 11,9 14,12 11,15",
    # Controls
    0xE231: "4,6 20,6 | 4,12 20,12 | 4,18 20,18 | 8,3 8,9 | 16,9 16,15 | 11,15 11,21",
    # References
    0xE232: "9,16 6,19 3,16 3,12 9,6 13,6 15,8 | 9,16 13,18 21,10 21,6 18,3 15,3 | 8,14 16,8",
    # Source
    0xE280: "4,9 4,4 20,4 20,9 4,9 | 12,9 12,20 | 8,16 12,20 16,16",
    # Destination
    0xE281: "4,15 4,20 20,20 20,15 4,15 | 12,3 12,13 | 8,9 12,13 16,9",
    # Data reference
    0xE282: "4,6 7,4 14,4 17,6 14,8 7,8 4,6 | 4,6 4,15 7,17 11,17 | 4,10 7,12 11,12 | 14,19 21,12 | 17,12 21,12 21,16",
    # Text
    0xE210: "5,4 19,4 19,20 5,20 5,4 | 8,8 16,8 | 8,12 16,12 | 8,16 13,16",
    # Value
    0xE211: "6,13 9,16 15,8 | 5,4 19,4 21,6 21,18 19,20 5,20 3,18 3,6 5,4",
    # Items
    0xE212: "4,5 8,5 8,9 4,9 4,5 | 11,5 15,5 15,9 11,9 11,5 | 16,15 20,15 20,19 16,19 16,15 | 5,15 9,15 9,19 5,19 5,15",
    # Accessible name
    0xE2A0: "3,8 9,8 13,4 13,20 9,16 3,16 3,8 | 16,8 19,12 16,16 | 20,7 22,12 20,17",
    # Description
    0xE2A1: "4,4 20,4 20,16 11,16 6,20 6,16 4,16 4,4 | 7,8 17,8 | 7,12 14,12",
    # Role
    0xE2A2: "4,7 9,4 15,4 20,7 19,16 15,20 9,20 5,16 4,7 | 8,10 | 16,10 | 9,15 12,17 15,15",
    # Editable
    0xE240: "4,19 6,13 16,3 21,8 11,18 4,19 | 13,6 18,11",
    # Selectable
    0xE241: "3,4 16,4 16,15 3,15 3,4 | 9,8 11,11 15,6 | 13,19 19,19 19,13",
    # Expandable
    0xE242: "4,10 4,4 10,4 | 14,4 20,4 20,10 | 4,14 4,20 10,20 | 20,14 20,20 14,20 | 8,8 4,4 | 16,16 20,20",
    # Minimum
    0xE270: "4,19 20,19 | 12,4 12,15 | 8,11 12,15 16,11",
    # Maximum
    0xE271: "4,5 20,5 | 12,20 12,9 | 8,13 12,9 16,13",
    # Required
    0xE272: "12,3 21,19 3,19 12,3 | 12,9 12,13 | 12,16",
    # Value type
    0xE290: "4,8 4,4 8,4 | 16,4 20,4 20,8 | 20,16 20,20 16,20 | 8,20 4,20 4,16 | 12,7 17,16 7,16 12,7",
    # Format
    0xE291: "5,3 15,3 20,8 20,21 5,21 5,3 | 15,3 15,8 20,8 | 8,12 11,12 | 14,12 17,12 | 8,16 11,16 | 14,16 17,16",
    # Pattern
    0xE292: "4,7 8,7 8,4 12,4 12,7 16,7 16,4 20,4 | 4,17 8,17 8,14 12,14 12,17 16,17 16,14 20,14",
    # Press event
    0xE260: "10,15 10,8 13,8 13,15 17,15 17,20 9,20 6,17 6,15 10,15 | 12,3 | 6,5 | 18,5",
    # Change event
    0xE261: "4,7 19,7 | 15,3 19,7 15,11 | 20,17 5,17 | 9,13 5,17 9,21",
    # Input event
    0xE262: "8,5 20,5 20,19 8,19 8,16 | 8,5 8,8 | 3,12 16,12 | 12,8 16,12 12,16 | 4,5 | 4,19",
    # Toggle
    0xE250: "7,7 17,7 21,10 21,14 17,17 7,17 3,14 3,10 7,7 | 15,10 18,12 15,14 12,12 15,10",
    # Submit
    0xE251: "4,12 4,20 20,20 20,12 | 12,16 12,4 | 8,8 12,4 16,8",
    # Navigate
    0xE252: "4,16 20,4 16,20 12,14 4,16 | 12,14 20,4",
    # Action
    0xE253: "13,3 5,13 11,13 10,21 19,10 13,10 13,3",
    # Duration
    0xE2B0: "4,6 4,18 | 20,6 20,18 | 4,12 20,12",
    # Interval
    0xE2B1: "4,7 4,17 | 12,7 12,17 | 20,7 20,17 | 4,12 20,12",
    # Delay
    0xE2B2: "6,4 18,4 | 6,20 18,20 | 7,4 7,8 17,16 17,20 | 17,4 17,8 7,16 7,20",
}


def draw_pictogram(pen, outline):
    def point_on_grid(point):
        x, y = (int(axis) for axis in point.split(","))
        return 48 + 22 * x, 655 - 22 * y

    for path in outline.split("|"):
        points = [point_on_grid(point) for point in path.split()]
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            length = hypot(x2 - x1, y2 - y1)
            nx = round(18 * (y2 - y1) / length)
            ny = round(18 * (x1 - x2) / length)
            polygon(pen, [(x1 - nx, y1 - ny), (x2 - nx, y2 - ny),
                          (x2 + nx, y2 + ny), (x1 + nx, y1 + ny)])
        # Small octagons join strokes and also draw standalone dots.
        for x, y in points:
            radius = 27 if len(points) == 1 else 18
            corner = round(radius * 0.42)
            polygon(pen, [(x - corner, y - radius), (x - radius, y - corner),
                          (x - radius, y + corner), (x - corner, y + radius),
                          (x + corner, y + radius), (x + radius, y + corner),
                          (x + radius, y - corner), (x + corner, y - radius)])


def build_font(destination):
    symbols = {
        0xE000: ("button", 900, button),
        0xE100: ("focused", 520, focused),
        0xE101: ("pressed", 520, pressed),
        0xE102: ("disabled", 520, disabled),
    }
    state_shapes = {0xE103: active, 0xE104: selected}
    components = json.loads(destination.with_name("components.json").read_text())
    outlines = PROPERTY_OUTLINES.copy()
    for entry in components:
        code = int(entry["code"], 16)
        if code == 0xE000:
            continue
        outlines[code] = entry["outline"]
        symbols[code] = (f"uni{code:04X}", 620, None)

    catalog = json.loads(destination.with_name("symbols.json").read_text())
    for entry in catalog:
        code = int(entry["code"], 16)
        if code in symbols:
            continue
        if entry["kind"] == "State":
            symbols[code] = (entry["label"].lower(), 520, state_shapes[code])
        else:
            symbols[code] = (f"uni{code:04X}", 620, None)

    glyphs = {".notdef": TTGlyphPen(None).glyph()}
    metrics = {".notdef": (520, 0)}
    for code, (name, advance, draw) in symbols.items():
        pen = TTGlyphPen(None)
        if draw is None:
            draw_pictogram(pen, outlines[code])
        else:
            draw(pen)
        glyph = pen.glyph()
        if draw is None:
            glyph.flags[0] |= flagOverlapSimple
        glyph.recalcBounds(None)
        glyphs[name] = glyph
        metrics[name] = (advance, glyph.xMin)

    builder = FontBuilder(1000, isTTF=True)
    builder.setupGlyphOrder(list(glyphs))
    builder.setupCharacterMap({code: entry[0] for code, entry in symbols.items()})
    builder.setupGlyf(glyphs)
    builder.setupHorizontalMetrics(metrics)
    builder.setupHorizontalHeader(ascent=800, descent=-200)
    builder.setupNameTable({
        "familyName": "Bitiato UI",
        "styleName": "Regular",
        "uniqueFontIdentifier": "Bitiato UI 0.4",
        "fullName": "Bitiato UI Regular",
        "psName": "BitiatoUI-Regular",
        "version": "Version 0.4",
    })
    builder.setupOS2(sTypoAscender=800, sTypoDescender=-200,
                     usWinAscent=800, usWinDescent=200)
    builder.setupPost()
    builder.font["head"].fontRevision = 0.4
    builder.font.recalcTimestamp = False
    builder.font["head"].created = builder.font["head"].modified = 2082844800
    builder.save(destination)
    browser_components = [
        {key: entry[key] for key in ("code", "label", "group")} for entry in components
    ]
    destination.with_name("symbols.js").write_text(
        "/* Generated by build_font.py. */\n"
        + "".join(
            "// prettier-ignore\nconst " + name + " = "
            + json.dumps(entries, ensure_ascii=True, separators=(",", ":")) + ";\n"
            for name, entries in (("catalog", catalog), ("components", browser_components))
        )
    )


if __name__ == "__main__":
    build_font(Path(__file__).with_name("bitiato_ui.ttf"))
