from time import sleep

from framebuf import FrameBuffer

from utils import Color, Position, Rect, split_rect, RectHigh, RectLow
from waveshare import LCD3inch5


def logo(display: FrameBuffer):
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


def update_display(lcd: LCD3inch5, draw_list: list, bg=Color.WHITE):
    """
    Update LCD, both high and low.

    :param lcd: LCD instance
    :param draw_list: list or drawings
    :param bg: background color, default white
    """
    lcd.fill(bg)
    for up in [upper for upper in draw_list if isinstance(upper, RectHigh)]:
        lcd.fill_rect(*up)
    lcd.show_up()

    lcd.fill(bg)
    for low in [lower for lower in draw_list if isinstance(lower, RectLow)]:
        lcd.fill_rect(*low)
    lcd.show_down()


def show_keyboard():
    """Show clickable keyboard icon."""
    lcd = LCD3inch5()
    lcd.backlight(20)
    key_draw = []
    while True:
        coord = lcd.get_touchpoint()
        if coord is not None:
            if coord.y < 32:
                if 420 < coord.x < 480:
                    key_draw = keyboard_icon(Position.SE, True)
        else:
            key_draw = keyboard_icon(Position.SE)
        update_display(lcd, key_draw)
        sleep(0.1)


def keyboard_icon(pos=Position.SE, invert=False):
    """
    Show keyboard icon.

    :param pos: 'SE', 'NW', 'NE', 'SW'
    :param invert: invert colors
    """
    foreground = Color.BLACK
    background = Color.WHITE
    if invert:
        foreground = Color.WHITE
        background = Color.BLACK
    ico_w, ico_h = 68, 32
    dpl_w, dpl_h = 480, 320
    if pos == Position.SE:
        pos_x, pos_y = dpl_w, dpl_h
    elif pos == Position.NW:
        pos_x, pos_y = ico_w, ico_h
    elif pos == Position.SW:
        pos_x, pos_y = ico_w, dpl_h
    elif pos == Position.NE:
        pos_x, pos_y = dpl_w, ico_h
    x = pos_x - ico_w
    y = pos_y - ico_h

    keyboard = split_rect(Rect(x, y, ico_w, ico_h, foreground))
    keyboard.extend(split_rect(Rect(x, y, ico_w, ico_h, foreground)))
    keyboard.extend(split_rect(Rect(x + 2, y + 2, ico_w - 4, ico_h - 4, background)))
    for i in range(6):
        keyboard.extend(split_rect(Rect(10 * i + x + 6, y + 6, 4, 4, foreground)))
        keyboard.extend(split_rect(Rect(10 * i + x + 6, y + 14, 4, 4, foreground)))
        keyboard.extend(split_rect(Rect(10 * i + x + 6, y + 22, 4, 4, foreground)))
    keyboard.extend(split_rect(Rect(x + 18, y + 22, 28, 4, foreground)))
    return keyboard


def demo_split_rect():
    """Show how to use split rect function."""
    lcd = LCD3inch5()
    lcd.backlight(20)

    rects = split_rect(Rect(40, 80, 40, 40, Color.BLUE))
    rects.extend(split_rect(Rect(40, 140, 40, 40, Color.GREEN)))
    rects.extend(split_rect(Rect(40, 200, 40, 40, Color.RED)))

    lcd.fill(Color.WHITE)
    for up in [upper for upper in rects if isinstance(upper, RectHigh)]:
        lcd.fill_rect(*up)
    lcd.show_up()

    lcd.fill(Color.WHITE)
    for low in [lower for lower in rects if isinstance(lower, RectLow)]:
        lcd.fill_rect(*low)
    lcd.show_down()


if __name__ == '__main__':
    show_keyboard()
    # demo_split_rect()
    # main()
    # pico_serial()
