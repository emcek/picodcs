from time import sleep
from waveshare import LCD3inch5


def main():
    lcd = LCD3inch5()
    lcd.backlight(20)
    lcd.fill(lcd.WHITE)
    lcd.fill_rect(140, 5, 200, 30, lcd.RED)
    lcd.text("Raspberry Pi Pico", 170, 17, lcd.WHITE)
    display_color = 0x001F
    lcd.text("3.5' IPS LCD TEST", 170, 57, lcd.BLACK)
    for i in range(12):
        lcd.fill_rect(i * 30 + 60, 100, 30, 50, display_color)
        display_color = display_color << 1
    lcd.show_up()
    while True:
        get = lcd.touch_get()
        if get is not None:
            x_point = int((get[1] - 430) * 480 / 3270)
            if x_point > 480:
                x_point = 480
            elif x_point < 0:
                x_point = 0
            y_point = 320 - int((get[0] - 430) * 320 / 3270)
            if y_point > 220:
                lcd.fill(lcd.WHITE)
                if x_point < 120:
                    lcd.fill_rect(0, 60, 120, 100, lcd.RED)
                    lcd.text("Button0", 20, 110, lcd.WHITE)
                elif x_point < 240:
                    lcd.fill_rect(120, 60, 120, 100, lcd.RED)
                    lcd.text("Button1", 150, 110, lcd.WHITE)
                elif x_point < 360:
                    lcd.fill_rect(240, 60, 120, 100, lcd.RED)
                    lcd.text("Button2", 270, 110, lcd.WHITE)
                else:
                    lcd.fill_rect(360, 60, 120, 100, lcd.RED)
                    lcd.text("Button3", 400, 110, lcd.WHITE)
        else:
            lcd.fill(lcd.WHITE)
            lcd.text("Button0", 20, 110, lcd.BLACK)
            lcd.text("Button1", 150, 110, lcd.BLACK)
            lcd.text("Button2", 270, 110, lcd.BLACK)
            lcd.text("Button3", 400, 110, lcd.BLACK)

        lcd.show_down()
        sleep(0.1)


if __name__ == '__main__':
    main()
