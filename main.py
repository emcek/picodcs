import sys
from time import sleep

import micropython

from utils import Rect, split_rect, RectHigh, RectLow
from waveshare import LCD3inch5

RED = micropython.const(0x07E0)
GREEN = micropython.const(0x001f)
BLUE = micropython.const(0xf800)
WHITE = micropython.const(0xffff)
BLACK = micropython.const(0x0000)


@micropython.native
def show_icon(ico: str, lcd: LCD3inch5, pos='SE', w=32, h=32, invert=False):
    """
    Show icon in general position at LCD.

    :param ico: icon name as string
    :param lcd: LCD instance
    :param pos: SE, SW, NE or NW
    :param w: width as int
    :param h: height as int
    :param invert: flip fg with bg
    """
    fg = BLACK
    bg = WHITE
    if invert:
        fg = WHITE
        bg = BLACK
    ico_w, ico_h = w, h
    dpl_w, dpl_h = 480, 160
    if pos == 'SE':
        pos_x, pos_y = dpl_w, dpl_h
    elif pos == 'NW':
        pos_x, pos_y = ico_w, ico_h
    elif pos == 'SW':
        pos_x, pos_y = ico_w, dpl_h
    elif pos == 'NE':
        pos_x, pos_y = dpl_w, ico_h
    x = pos_x - ico_w
    y = pos_y - ico_h
    if ico == 'logo':
        logo(lcd, x, y, ico_w, ico_h, fg, bg)
    elif ico == 'keyboard':
        keyboard(lcd, x, y, ico_w, ico_h, fg, bg)


@micropython.native
def logo(display: LCD3inch5, x: int, y: int, ico_w: int, ico_h: int, fg: int, bg: int):
    """
    Draw MircoPython logo at LCD.

    :param display: lcd instance
    :param x: position X
    :param y: position Y
    :param ico_w: icon width
    :param ico_h: icon height
    :param fg: foreground color
    :param bg: background color
    """
    display.fill_rect(x, y, ico_w, ico_h, fg)
    display.fill_rect(x + 2, y + 2, ico_w - 4, ico_h - 4, bg)
    display.vline(x + 9, y + 8, 22, fg)
    display.vline(x + 16, y + 2, 22, fg)
    display.vline(x + 23, y + 8, 22, fg)
    display.fill_rect(x + 26, y + 24, 2, 4, fg)


@micropython.native
def keyboard(display: LCD3inch5, x: int, y: int, ico_w: int, ico_h: int, fg: int, bg: int):
    """
    Draw keyboard icon.

    :param display: lcd instance
    :param x: position X
    :param y: position Y
    :param ico_w: icon width
    :param ico_h: icon height
    :param fg: foreground color
    :param bg: background color
    """
    display.fill_rect(x, y, ico_w, ico_h, fg)
    display.fill_rect(x, y, ico_w, ico_h, fg)
    display.fill_rect(x + 2, y + 2, ico_w - 4, ico_h - 4, bg)
    for i in range(6):
        display.fill_rect(10 * i + x + 6, y + 6, 4, 4, fg)
        display.fill_rect(10 * i + x + 6, y + 14, 4, 4, fg)
        display.fill_rect(10 * i + x + 6, y + 22, 4, 4, fg)
    display.fill_rect(x + 18, y + 22, 28, 4, fg)


@micropython.native
def show_keyboard():
    """Demo code form Waveshare."""
    lcd = LCD3inch5()
    lcd.backlight(20)
    lcd.fill(WHITE)
    lcd.show_up()
    while True:
        coord = lcd.get_touchpoint()
        if 0 < coord.y < 32 and 420 < coord.x < 480:
            show_icon('keyboard', lcd, 'SE', w=68, h=32, invert=True)
            show_icon('logo', lcd, 'NW', w=32, h=32)
            lcd.text(sys.version, 0, 40, BLACK)
            lcd.text(sys.implementation._machine, 0, 50, BLACK)
        else:
            lcd.fill(WHITE)
            show_icon('keyboard', lcd, 'SE', w=68, h=32)
        lcd.show_down()
        sleep(0.1)


def demo_split_rect():
    """Show how to use split rect function."""
    lcd = LCD3inch5()
    lcd.backlight(20)

    rects = split_rect(Rect(40, 80, 40, 40, BLUE))
    rects.extend(split_rect(Rect(40, 140, 40, 40, GREEN)))
    rects.extend(split_rect(Rect(40, 200, 40, 40, RED)))

    high = [upper for upper in rects if isinstance(upper, RectHigh)]
    low = [lower for lower in rects if isinstance(lower, RectLow)]
    if high:
        lcd.fill(WHITE)
        for up in high:
            lcd.fill_rect(up.x, up.y, up.w, up.h, up.c)
        lcd.show_up()
    if low:
        lcd.fill(WHITE)
        for down in low:
            lcd.fill_rect(down.x, down.y, down.w, down.h, down.c)
        lcd.show_down()


if __name__ == '__main__':
    show_keyboard()
    # demo_split_rect()
