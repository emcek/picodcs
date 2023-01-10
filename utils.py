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
Rect = namedtuple('Rect', ('x', 'y', 'w', 'h', 'c'))
RectLow = namedtuple('RectLow', ('x', 'y', 'w', 'h', 'c'))
RectHigh = namedtuple('RectHigh', ('x', 'y', 'w', 'h', 'c'))


def split_rect(rect: Rect, split=160):
    """
    Split rectangle between high and low part.

    :param rect: rectangle tuple as Rect
    :param split: default 160
    :return: List of RectLow, RectHigh or None
    """
    y1_mod = rect.y % split
    y1_div = rect.y // split
    y2_mod = (rect.y + rect.h) % split
    y2_div = (rect.y + rect.h) // split
    lower, upper = None, None

    if not y1_div and not y2_div:
        upper = RectHigh(rect.x, rect.y, rect.w, rect.h, rect.c)
    elif y1_div and y2_div:
        lower = RectLow(rect.x, y1_mod, rect.w, rect.h, rect.c)
    elif not y1_div and y2_div:
        upper = RectHigh(rect.x, rect.y, rect.w, rect.h - y2_mod, rect.c)
        lower = RectLow(rect.x, 0, rect.w, y2_mod, rect.c)
    return [upper, lower]
