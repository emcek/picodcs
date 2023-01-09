import gc
from sys import stdin
from time import sleep, sleep_ms

import framebuf
import uselect
from machine import Pin

from utils import Color
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


# size of each letter in pixels
CHARACTER_SIZE = 8

# how serial lines are ended
TERMINATOR = "\n"


class Pico:
    """Pico class."""
    def __init__(self):
        """
        Run any once-off startup tasks.

        Set up the global LCD object.
        Set up input.
        """
        self.lcd = LCD3inch5()

        self.lcd.fill(0x0000)
        self.lcd.text("loading...", 1, 1, 0xFFFF)
        self.lcd.show_up()

        self.key_a = Pin(15, Pin.IN, Pin.PULL_UP)
        # interrupt
        self.key_a.irq(trigger=Pin.IRQ_FALLING, handler=self.on_key_a_pressed)
        self.key_b = Pin(17, Pin.IN, Pin.PULL_UP)
        self.key_up = Pin(2, Pin.IN, Pin.PULL_UP)
        self.key_center = Pin(3, Pin.IN, Pin.PULL_UP)
        self.key_left = Pin(16, Pin.IN, Pin.PULL_UP)
        self.key_down = Pin(18, Pin.IN, Pin.PULL_UP)
        self.key_right = Pin(20, Pin.IN, Pin.PULL_UP)

        self.key_a_pressed = False
        self.key_b_pressed = False
        self.key_up_pressed = False
        self.key_center_pressed = False
        self.key_left_pressed = False
        self.key_down_pressed = False
        self.key_right_pressed = False

        # give a chance to break the boot to fix serial/code issues. Put any riskier startup code after this
        boot_delay_seconds = 5
        self.lcd.text(
            f"press A+B within {boot_delay_seconds} seconds to", 1, 11, 0xFFFF
        )
        self.lcd.text("cancel boot...", 1, 21, 0xFFFF)
        self.lcd.show_up()

        self.run_loop = True

        # store incomplete lines from serial here. list of strings (no typing module in micropython)
        self.buffered_input = []
        # when we get a full line store it here, without the terminator.
        # gets overwritten if a new line is read (as early as next tick).
        # blanked each tick.
        self.input_line_this_tick = ""

    def main(self):
        """
        Code entrypoint.

        The function that gets called to start.
        All non-setup code here or in functions under it.
        """
        background_color = 0xB642F5
        counter = 0

        latest_input_line = ""

        # main loop
        while self.run_loop:

            # single background per tick
            self.lcd.fill(background_color)

            # record whether the buttons are pressed or not this tick.
            # see docstring for global variable to read from
            self.read_input()
            # buffer from the USB to serial port
            self.read_serial_input()

            # app per tick code here

            # debug ram issues
            # self.lcd.text(str(gc.mem_free()), 1, self.lcd.height - 9, 0xFFFF)

            # simple output test
            counter += 1
            self.lcd.text(str(counter), 5, 5, 0xFFFF)

            # show serial input on the screen.
            # only update if we have a new line
            if self.input_line_this_tick:
                latest_input_line = self.input_line_this_tick
            self.lcd.text(latest_input_line, 5, 14, 0xFFFF)

            # end app per tick code here

            # single draw call at the end of each tick
            self.lcd.show_down()

            # quit program to avoid locking serial up if specified
            if self.key_a_pressed and self.key_b_pressed:
                self.exit()

            # simple loop speed control
            sleep_ms(100)

    def read_input(self):
        """
        Records which keys are pressed or not.

        Global variables key_<a,b,2,3,4,5,6>_pressed will be set to True or False for reading by other code.
        """
        # 0 means pressed
        self.key_a_pressed = self.key_a.value() == 0
        self.key_b_pressed = self.key_b.value() == 0
        self.key_up_pressed = self.key_up.value() == 0
        self.key_center_pressed = self.key_center.value() == 0
        self.key_left_pressed = self.key_left.value() == 0
        self.key_down_pressed = self.key_down.value() == 0
        self.key_right_pressed = self.key_right.value() == 0

    def read_serial_input(self):
        """
        Buffers serial input.

        Writes it to input_line_this_tick when we have a full line.
        Clears input_line_this_tick otherwise.
        """
        # stdin.read() is blocking which means we hang here if we use it. Instead use select to tell us if there's anything available
        # note: select() is deprecated. Replace with Poll() to follow best practises
        select_result = uselect.select([stdin], [], [], 0)
        while select_result[0]:
            # there's no easy micropython way to get all the bytes.
            # instead get the minimum there could be and keep checking with select and a while loop
            input_character = stdin.read(1)
            # add to the buffer
            self.buffered_input.append(input_character)
            # check if there's any input remaining to buffer
            select_result = uselect.select([stdin], [], [], 0)
        # if a full line has been submitted
        if TERMINATOR in self.buffered_input:
            line_ending_index = self.buffered_input.index(TERMINATOR)
            # make it available
            self.input_line_this_tick = "".join(self.buffered_input[:line_ending_index])
            # remove it from the buffer.
            # If there's remaining data, leave that part. This removes the earliest line so should allow multiple lines buffered in a tick to work.
            # however if there are multiple lines each tick, the buffer will continue to grow.
            if line_ending_index < len(self.buffered_input):
                self.buffered_input = self.buffered_input[line_ending_index + 1:]
            else:
                self.buffered_input = []
        # otherwise clear the last full line so subsequent ticks can infer the same input is new input (not cached)
        else:
            self.input_line_this_tick = ""

    def exit(self):
        """Exit."""
        self.run_loop = False

    def on_key_a_pressed(self, p):
        """When button is pressed."""
        print("key a pressed: ", p)


def pico_serial():
    """Run Pico example."""
    pico = Pico()
    pico.main()
    # when the above exits, clean up
    gc.collect()


def logo(display: framebuf.FrameBuffer):
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


def main2():
    """Demo code form Waveshare."""
    lcd = LCD3inch5()
    lcd.backlight(20)
    lcd.fill(Color.WHITE)
    keyboard_icon(lcd, 'SE')
    lcd.show_down()
    while True:
        coord = lcd.get_touchpoint()
        if coord is not None:
            if coord.y < 32:
                if 420 < coord.x < 480:
                    lcd.fill_rect(lcd.width - 68, lcd.height - 32, 68, 32, Color.RED)
        else:
            lcd.fill(Color.WHITE)
            keyboard_icon(lcd, 'SE')
        lcd.show_down()
        sleep(0.1)


def keyboard_icon(lcd, pos='SE'):
    """
    Show keyboard icon.

    :param lcd: LDC instance
    :param pos: 'SE' or 'NW'
    """
    if pos == 'SE':
        # keyboard icon down right
        lcd.fill_rect(lcd.width - 68, lcd.height - 32, 68, 32, Color.BLACK)
        lcd.fill_rect(lcd.width - 66, lcd.height - 30, 64, 28, Color.WHITE)
        for i in range(6):
            lcd.fill_rect(10 * i + lcd.width - 60, lcd.height - 10, 4, 4, Color.BLACK)
            lcd.fill_rect(10 * i + lcd.width - 60, lcd.height - 18, 4, 4, Color.BLACK)
            lcd.fill_rect(10 * i + lcd.width - 60, lcd.height - 26, 4, 4, Color.BLACK)
        lcd.fill_rect(lcd.width - 48, lcd.height - 10, 28, 4, Color.BLACK)
    elif pos == 'NW':
        # keyboard icon upper left
        lcd.fill_rect(0, 0, 68, 32, Color.BLACK)
        lcd.fill_rect(2, 2, 64, 28, Color.WHITE)
        for i in range(6):
            lcd.fill_rect(10 * i + 6, 6, 4, 4, Color.BLACK)
            lcd.fill_rect(10 * i + 6, 14, 4, 4, Color.BLACK)
            lcd.fill_rect(10 * i + 6, 22, 4, 4, Color.BLACK)
        lcd.fill_rect(18, 22, 28, 4, Color.BLACK)


if __name__ == '__main__':
    main2()
    # main()
    # pico_serial()
