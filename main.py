import gc
from time import sleep

from framebuf import FrameBuffer

from pico import Pico
from utils import Color, Position, Rect, split_rect
from waveshare import LCD3inch5


def main():
    """Demo code form Waveshare."""
    lcd = LCD3inch5()
    lcd.backlight(20)
    lcd.fill(Color.WHITE)
    lcd.fill_rect(140, 5, 200, 30, Color.RED)
    lcd.text("Raspberry Pi Pico", 170, 17, Color.WHITE)
    display_color = 0x001F
    lcd.text("3.5' IPS LCD TEST", 170, 57, Color.BLACK)
    for i in range(12):
        lcd.fill_rect(i * 30 + 60, 100, 30, 50, display_color)
        display_color = display_color << 1
    logo(lcd)
    lcd.show_up()
    while True:
        coord_x_y = lcd.absolute_coord()
        if coord_x_y is not None:
            x_point = int((coord_x_y[0] - 430) * 480 / 3270)
            y_point = int((coord_x_y[1] - 430) * 320 / 3270)
            print('****', f'x: {x_point:>3} y: {y_point:>3}\n')
        else:
            lcd.fill(Color.WHITE)
            lcd.text("Button0", 20, 110, Color.BLACK)
            lcd.text("Button1", 150, 110, Color.BLACK)
            lcd.text("Button2", 270, 110, Color.BLACK)
            lcd.text("Button3", 400, 110, Color.BLACK)

        lcd.show_down()
        sleep(0.1)


def pico_serial():
    """Run Pico example."""
    pico = Pico()
    pico.main()
    # when the above exits, clean up
    gc.collect()


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


def show_keyboard():
    """Show clickable keyboard icon."""
    lcd = LCD3inch5()
    lcd.backlight(20)
    lcd.fill(Color.WHITE)
    while True:
        coord = lcd.get_touchpoint()
        if coord is not None:
            if coord.y < 32:
                if 420 < coord.x < 480:
                    keyboard_icon(lcd, Position.SW, True)
        else:
            lcd.fill(Color.WHITE)
            keyboard_icon(lcd, Position.SW)
        lcd.show_down()
        sleep(0.1)


def keyboard_icon(lcd: LCD3inch5, pos=Position.SE, invert=False):
    """
    Show keyboard icon.

    :param lcd: LCD instance
    :param pos: 'SE', 'NW', 'NE', 'SW'
    :param invert: invert colors
    """
    foreground = Color.BLACK
    background = Color.WHITE
    if invert:
        foreground = Color.WHITE
        background = Color.BLACK
    ico_w, ico_h = 68, 32
    if pos == Position.SE:
        pos_x, pos_y = 480, 160
    elif pos == Position.NW:
        pos_x, pos_y = 68, 32
    elif pos == Position.SW:
        pos_x, pos_y = 68, 160
    elif pos == Position.NE:
        pos_x, pos_y = 480, 32

    x = pos_x - ico_w
    y = pos_y - ico_h
    lcd.fill_rect(x, y, ico_w, ico_h, foreground)
    lcd.fill_rect(x + 2, y + 2, ico_w - 4, ico_h - 4, background)
    for i in range(6):
        lcd.fill_rect(10 * i + x + 6, y + 6, 4, 4, foreground)
        lcd.fill_rect(10 * i + x + 6, y + 14, 4, 4, foreground)
        lcd.fill_rect(10 * i + x + 6, y + 22, 4, 4, foreground)
    lcd.fill_rect(x + 18, y + 22, 28, 4, foreground)


def demo_split_rect():
    """Show how to use split rect function."""
    lcd = LCD3inch5()
    lcd.backlight(20)

    upper1, lower1 = split_rect(Rect(40, 80, 40, 40))
    upper2, lower2 = split_rect(Rect(40, 140, 40, 40))
    upper3, lower3 = split_rect(Rect(40, 200, 40, 40))

    uppers = [upper for upper in (upper1, upper2, upper3) if upper is not None]
    lowers = [lower for lower in (lower1, lower2, lower3) if lower is not None]

    if any(uppers):
        lcd.fill(Color.WHITE)
        for upper in uppers:
            lcd.fill_rect(upper.x, upper.y, upper.w, upper.h, Color.BLUE)
        lcd.show_up()

    if any(lowers):
        lcd.fill(Color.WHITE)
        for lower in lowers:
            lcd.fill_rect(lower.x, lower.y, lower.w, lower.h, Color.RED)
        lcd.show_down()


if __name__ == '__main__':
    show_keyboard()
    # demo_split_rect()
    # main()
    # pico_serial()
