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
Rect = namedtuple('Rect', ('x', 'y', 'w', 'h'))


def split_rect(rect: Rect, height=160):
    """
    Split rectangle between upper and lower part.

    :param rect:
    :param height: default 160
    :return: Tuple of Rect or None
    """
    y1_mod = rect.y % height
    y1_div = rect.y // height
    y2_mod = (rect.y + rect.h) % height
    y2_div = (rect.y + rect.h) // height
    lower, upper = None, None

    if not y1_div and not y2_div:
        upper = rect
    elif y1_div and y2_div:
        lower = Rect(rect.x, y1_mod, rect.w, rect.h)
    elif not y1_div and y2_div:
        upper = Rect(rect.x, rect.y, rect.w, rect.h - y2_mod)
        lower = Rect(rect.x, 0, rect.w, y2_mod)
    return upper, lower
