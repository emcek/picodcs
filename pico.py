import uselect
from machine import Pin
from time import sleep_ms
from waveshare import LCD3inch5
from sys import stdin

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
