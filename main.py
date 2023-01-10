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
    """Show clickable keyborad icon."""
    lcd = LCD3inch5()
    lcd.backlight(20)
    lcd.fill(Color.WHITE)
    keyboard_icon(lcd, Position.SE)
    lcd.show_down()
    while True:
        coord = lcd.get_touchpoint()
        if coord is not None:
            if coord.y < 32:
                if 420 < coord.x < 480:
                    # lcd.fill_rect(lcd.width - 68, lcd.height - 32, 68, 32, Color.RED)
                    keyboard_icon(lcd, Position.SE, True)
        else:
            lcd.fill(Color.WHITE)
            keyboard_icon(lcd, Position.SE)
        lcd.show_down()
        sleep(0.1)


def keyboard_icon(lcd: LCD3inch5, pos=Position.SE, invert=False):
    """
    Show keyboard icon.

    :param lcd: LDC instance
    :param pos: 'SE' or 'NW'
    :param invert: invert colors
    """
    foreground = Color.BLACK
    background = Color.WHITE
    if invert:
        foreground = Color.WHITE
        background = Color.BLACK

    if pos == Position.SE:
        # keyboard icon lower right
        lcd.fill_rect(lcd.width - 68, lcd.height - 32, 68, 32, foreground)
        lcd.fill_rect(lcd.width - 66, lcd.height - 30, 64, 28, background)
        for i in range(6):
            lcd.fill_rect(10 * i + lcd.width - 60, lcd.height - 10, 4, 4, foreground)
            lcd.fill_rect(10 * i + lcd.width - 60, lcd.height - 18, 4, 4, foreground)
            lcd.fill_rect(10 * i + lcd.width - 60, lcd.height - 26, 4, 4, foreground)
        lcd.fill_rect(lcd.width - 48, lcd.height - 10, 28, 4, foreground)
    elif pos == Position.NW:
        # keyboard icon upper left
        lcd.fill_rect(0, 0, 68, 32, foreground)
        lcd.fill_rect(2, 2, 64, 28, background)
        for i in range(6):
            lcd.fill_rect(10 * i + 6, 6, 4, 4, foreground)
            lcd.fill_rect(10 * i + 6, 14, 4, 4, foreground)
            lcd.fill_rect(10 * i + 6, 22, 4, 4, foreground)
        lcd.fill_rect(18, 22, 28, 4, foreground)


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
    # show_keyboard()
    demo_split_rect()
    # main()
    # pico_serial()
