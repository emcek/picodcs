from collections import namedtuple


class Color:
    RED = 0x07E0
    GREEN = 0x001f
    BLUE = 0xf800
    WHITE = 0xffff
    BLACK = 0x0000


Coord = namedtuple('Coord', ('x', 'y'))
