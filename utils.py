from collections import namedtuple


class Color:
    """Basic colors values in hex."""
    RED = 0x07E0
    GREEN = 0x001f
    BLUE = 0xf800
    WHITE = 0xffff
    BLACK = 0x0000


class Position:
    """Position primitives."""
    N = 'N'
    NE = 'NE'
    E = 'E'
    SE = 'SE'
    S = 'S'
    SW = 'SW'
    W = 'W'
    NW = 'NW'


Coord = namedtuple('Coord', ('x', 'y'))
