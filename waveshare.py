from collections import namedtuple
from time import sleep_ms, sleep_us

import framebuf
from machine import Pin, SPI, PWM

LCD_DC = 8
LCD_CS = 9
LCD_SCK = 10
LCD_MOSI = 11
LCD_MISO = 12
LCD_BL = 13
LCD_RST = 15
TP_CS = 16
TP_IRQ = 17
Coord = namedtuple('Coord', ('x', 'y'))


class LCD3inch5(framebuf.FrameBuffer):
    """
    Waveshare 3.5" (480×320 Pixels, 65K colors) IPS LCD.

    * resistive touch
    * microSD slot through the SDIO interface
    * mini jack 3,5 mm,
    * photo-resistor
    * passive buzzer
    * RGB LED
    * PH2.0 battery header for connecting 3.7V Li-po battery

    Waveshare 20159: https://www.waveshare.com/pico-eval-board.htm
    """
    def __init__(self):
        """Initialize low level FrameBuffer."""
        self.RED = 0x07E0
        self.GREEN = 0x001f
        self.BLUE = 0xf800
        self.WHITE = 0xffff
        self.BLACK = 0x0000

        self.width = 480
        self.height = 160

        self.cs = Pin(LCD_CS, Pin.OUT)
        self.rst = Pin(LCD_RST, Pin.OUT)
        self.dc = Pin(LCD_DC, Pin.OUT)

        self.tp_cs = Pin(TP_CS, Pin.OUT)
        self.irq = Pin(TP_IRQ, Pin.IN)

        self.cs(1)
        self.dc(1)
        self.rst(1)
        self.tp_cs(1)
        self.spi = SPI(1, 60_000_000, sck=Pin(LCD_SCK), mosi=Pin(LCD_MOSI), miso=Pin(LCD_MISO))

        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

    def write_cmd(self, cmd):
        """
        Write command as integer.

        :param cmd:
        """
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        """
        Write data as integer.

        :param buf:
        """
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display."""
        self.rst(1)
        sleep_ms(5)
        self.rst(0)
        sleep_ms(10)
        self.rst(1)
        sleep_ms(5)
        self.write_cmd(0x21)
        self.write_cmd(0xC2)
        self.write_data(0x33)
        self.write_cmd(0XC5)
        self.write_data(0x00)
        self.write_data(0x1e)
        self.write_data(0x80)
        self.write_cmd(0xB1)
        self.write_data(0xB0)
        self.write_cmd(0x36)
        self.write_data(0x28)
        self.write_cmd(0XE0)
        self.write_data(0x00)
        self.write_data(0x13)
        self.write_data(0x18)
        self.write_data(0x04)
        self.write_data(0x0F)
        self.write_data(0x06)
        self.write_data(0x3a)
        self.write_data(0x56)
        self.write_data(0x4d)
        self.write_data(0x03)
        self.write_data(0x0a)
        self.write_data(0x06)
        self.write_data(0x30)
        self.write_data(0x3e)
        self.write_data(0x0f)
        self.write_cmd(0XE1)
        self.write_data(0x00)
        self.write_data(0x13)
        self.write_data(0x18)
        self.write_data(0x01)
        self.write_data(0x11)
        self.write_data(0x06)
        self.write_data(0x38)
        self.write_data(0x34)
        self.write_data(0x4d)
        self.write_data(0x06)
        self.write_data(0x0d)
        self.write_data(0x0b)
        self.write_data(0x31)
        self.write_data(0x37)
        self.write_data(0x0f)
        self.write_cmd(0X3A)
        self.write_data(0x55)
        self.write_cmd(0x11)
        sleep_ms(120)
        self.write_cmd(0x29)
        self.write_cmd(0xB6)
        self.write_data(0x00)
        self.write_data(0x62)
        self.write_cmd(0x36)
        self.write_data(0x28)

    def show_up(self):
        """Show Up."""
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0xdf)
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x9f)
        self.write_cmd(0x2C)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)

    def show_down(self):
        """Show Down."""
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0xdf)
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0xA0)
        self.write_data(0x01)
        self.write_data(0x3f)
        self.write_cmd(0x2C)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)

    @staticmethod
    def backlight(duty):
        """
        Set backlight.

        :param duty: 1-100 % as integer
        """
        pwm = PWM(Pin(LCD_BL))
        pwm.freq(1000)
        if duty >= 100:
            pwm.duty_u16(65535)
        else:
            pwm.duty_u16(655 * duty)

    def draw_point(self, x, y, color):
        """
        Draw a point.

        :param x: int
        :param y: int
        :param color: int
        """
        self.write_cmd(0x2A)
        self.write_data((x - 2) >> 8)
        self.write_data((x - 2) & 0xff)
        self.write_data(x >> 8)
        self.write_data(x & 0xff)

        self.write_cmd(0x2B)
        self.write_data((y - 2) >> 8)
        self.write_data((y - 2) & 0xff)
        self.write_data(y >> 8)
        self.write_data(y & 0xff)

        self.write_cmd(0x2C)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        for _ in range(9):
            h_color = bytearray(color >> 8)
            l_color = bytearray(color & 0xff)
            self.spi.write(h_color)
            self.spi.write(l_color)
        self.cs(1)

    def absolute_coord(self):
        """
        Get absolute coordinates (x and y) for touched point.

        :return: tuple of float coordinates: x and y
        """
        if self.irq() == 0:
            self.spi = SPI(1, baudrate=5_000_000, sck=Pin(LCD_SCK), mosi=Pin(LCD_MOSI), miso=Pin(LCD_MISO))
            self.tp_cs(0)
            point_x = 0
            point_y = 0
            for _ in range(3):
                self.spi.write(bytearray([0XD0]))
                read_date = self.spi.read(2)
                sleep_us(10)
                point_y = point_y + (((read_date[0] << 8) + read_date[1]) >> 3)
                # print(f'y {point_y:>6.1f}')

                self.spi.write(bytearray([0X90]))
                read_date = self.spi.read(2)
                # sleep_us(10)
                point_x = point_x + (((read_date[0] << 8) + read_date[1]) >> 3)
                # print(f'x {point_x:>6.1f}')

            point_x = point_x / 3
            point_y = point_y / 3

            self.tp_cs(1)
            self.spi = SPI(1, baudrate=60_000_000, sck=Pin(LCD_SCK), mosi=Pin(LCD_MOSI), miso=Pin(LCD_MISO))
            print('####', f'x: {point_x:>6.1f} y: {point_y:>6.1f}')
            return Coord(x=point_x, y=point_y)

    def get_touchpoint(self):
        """
        Get scaled coordinates: x and y.

        :return: tuple of int coordinates: x and y
        """
        coord = self.absolute_coord()
        if coord is not None:
            x_point = int((coord.x - 430) * 480 / 3270)
            y_point = int((coord.y - 430) * 320 / 3270)
            print('****', f'x: {x_point:>3} y: {y_point:>3}\n')
            return Coord(x=x_point, y=y_point)
