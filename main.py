from time import sleep

import micropython

from utils import Rect, split_rect, RectHigh, RectLow
from waveshare import LCD3inch5

RED = micropython.const(0x07E0)
GREEN = micropython.const(0x001f)
BLUE = micropython.const(0xf800)
WHITE = micropython.const(0xffff)
BLACK = micropython.const(0x0000)


def logo(display: LCD3inch5):
    """
    Show MircoPython logo at LCD.

    :param display: lcd instance
    """
    # display.fill(0)
    display.fill_rect(0, 0, 32, 32, 1)
    display.fill_rect(2, 2, 28, 28, 0)
    display.vline(9, 8, 22, 1)
    display.vline(16, 2, 22, 1)
    display.vline(23, 8, 22, 1)
    display.fill_rect(26, 24, 2, 4, 1)
    display.text('MicroPython', 40, 0, 1)
    display.text('Waveshare', 40, 12, 1)
    display.text('IPS 320x480', 40, 24, 1)


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
            keyboard_icon(lcd, 'SE', True)
        else:
            lcd.fill(WHITE)
            keyboard_icon(lcd, 'SE')
        lcd.show_down()
        sleep(0.1)


@micropython.native
def keyboard_icon(lcd: LCD3inch5, pos='SE', invert=False):
    """
    Show keyboard icon.

    :param lcd: Display instance
    :param pos: 'SE', 'NW', 'NE', 'SW'
    :param invert: invert colors
    """
    fg = BLACK
    bg = WHITE
    if invert:
        fg = WHITE
        bg = BLACK
    ico_w, ico_h = 68, 32
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

    lcd.fill_rect(x, y, ico_w, ico_h, fg)
    lcd.fill_rect(x, y, ico_w, ico_h, fg)
    lcd.fill_rect(x + 2, y + 2, ico_w - 4, ico_h - 4, bg)
    for i in range(6):
        lcd.fill_rect(10 * i + x + 6, y + 6, 4, 4, fg)
        lcd.fill_rect(10 * i + x + 6, y + 14, 4, 4, fg)
        lcd.fill_rect(10 * i + x + 6, y + 22, 4, 4, fg)
    lcd.fill_rect(x + 18, y + 22, 28, 4, fg)


def demo_split_rect():
    """Show how to use split rect function."""
    lcd = LCD3inch5()
    lcd.backlight(20)

    rects = split_rect(Rect(40, 80, 40, 40, BLUE))
    rects.extend(split_rect(Rect(40, 140, 40, 40, GREEN)))
    rects.extend(split_rect(Rect(40, 200, 40, 40, RED)))

    lcd.fill(WHITE)
    for up in [upper for upper in rects if isinstance(upper, RectHigh)]:
        lcd.fill_rect(up.x, up.y, up.w, up.h, up.c)
    lcd.show_up()

    lcd.fill(WHITE)
    for low in [lower for lower in rects if isinstance(lower, RectLow)]:
        lcd.fill_rect(low.x, low.y, low.w, low.h, low.c)
    lcd.show_down()


if __name__ == '__main__':
    show_keyboard()
    # demo_split_rect()
