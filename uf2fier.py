#!/usr/bin/env python3

from sys import argv


class UF2Font:
    def __init__(self, name, data):
        self.data = {encoding: UF2Char(encoding, 0x00, [0x00] * 0x20)
                     for encoding in range(0x100)}
        self.name = name
        self.widths = [0x00] * 0x100

        for k, v in data.items():
            self.data[k] = v
            self.widths[k] = v.width

    def __repr__(self):
        width_lines = []

        for i in range(0, len(self.widths), 16):
            line = " ".join(
                f"{self.widths[j]:02x}{self.widths[j + 1]:02x}"
                for j in range(i, i + 16, 2)
            )
            width_lines.append(f"\t\t{line}")

        glyph_lines = "\n".join(str(char) for char in self.data.values())

        return (
            f"@Font-{self.name}\n"
            "\t&widths [\n"
            + "\n".join(width_lines) + " ]\n"
            "\t&glyphs [\n"
            + glyph_lines + " ]"
        )


class UF2Char:
    def __init__(self, code, width, data):
        self.code = code
        self.width = width
        self.data = tuple(data)

    def __repr__(self):
        return (
            ("\t\t( code: %02x, width: %02x )\n" % (self.code, self.width)) +
            "\t\t%02x%02x %02x%02x %02x%02x %02x%02x "
            "%02x%02x %02x%02x %02x%02x %02x%02x\n\t\t"
            "%02x%02x %02x%02x %02x%02x %02x%02x "
            "%02x%02x %02x%02x %02x%02x %02x%02x"
        ) % self.data

        return (
            f"( code: {self.code:02x}, width: {self.width:02x} )\n"
            "{data_lines}\n"
        )


def parse_bdf_file(input_file):
    with open(input_file, 'r') as file:
        data = {}
        name = input_file.split('.')[0]
        encoding = None
        width = 0
        bitmap = []
        in_bitmap = False
        i = 0

        for line in file:
            line = line.strip()

            if line.startswith('ENCODING'):
                encoding = int(line.split()[1])
                if encoding > 255:
                    encoding = None

            elif encoding is not None and line.startswith('DWIDTH'):
                width = int(line.split()[1])

            elif encoding is not None and line.startswith('BITMAP'):
                bitmap = [0x00] * 0x20
                in_bitmap = True
                i = 0

            elif in_bitmap:
                if line.startswith('ENDCHAR'):
                    data[encoding] = UF2Char(encoding, width, bitmap)
                    encoding = None
                    width = None
                    in_bitmap = False
                else:
                    bitmap[i] = int(line, 16)
                    i += 1

    return UF2Font(name, data)


font = parse_bdf_file(argv[1])

print(font)
