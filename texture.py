import struct
from gl import *
from vector import *


class Texture:
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        with open(self.path, "rb") as image:
            image.seek(2 + 4 + 2 + 2)
            header_size = struct.unpack("=l", image.read(4))[0]
            image.seek(2 + 4 + 2 + 2 + 4 + 4)
            self.width = struct.unpack("=l", image.read(4))[0]
            self.height = struct.unpack("=l", image.read(4))[0]

            image.seek(header_size)
            self.pixels = []
            self.normal = []
            for y in range(self.width):
                self.pixels.append([])
                self.normal.append([])
                for x in range(self.height):
                    b = ord(image.read(1))
                    g = ord(image.read(1))
                    r = ord(image.read(1))
                    self.pixels[y].append((b, g, r))
                    self.normal[y].append(
                        ((b / 255) * 2 - 1, (g / 255) * 2 - 1, (r / 255) * 2 - 1)
                    )
            image.close()

    def getColor(self, tx, ty):
        x = round(tx * self.width)
        y = round(ty * self.height)

        return self.pixels[y][x]

    def getColori(self, tx, ty, intensity):
        tx = round(tx)
        ty = round(ty)
        b = round(self.pixels[ty][tx][0] * intensity)
        g = round(self.pixels[ty][tx][1] * intensity)
        r = round(self.pixels[ty][tx][2] * intensity)

        return (
            max(min(b, 255), 0),
            max(min(g, 255), 0),
            max(min(r, 255), 0),
        )
