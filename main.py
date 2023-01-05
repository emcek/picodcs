from time import sleep
from waveshare import LCD3inch5


if __name__ == '__main__':
    LCD = LCD3inch5()
    LCD.backlight(20)
    # color BRG
    LCD.fill(LCD.WHITE)
    LCD.fill_rect(140, 5, 200, 30, LCD.RED)
    LCD.text("Raspberry Pi Pico", 170, 17, LCD.WHITE)
    display_color = 0x001F
    LCD.text("3.5' IPS LCD TEST", 170, 57, LCD.BLACK)
    for i in range(0, 12):
        LCD.fill_rect(i * 30 + 60, 100, 30, 50, display_color)
        display_color = display_color << 1
    LCD.show_up()

    while True:
        get = LCD.touch_get()
        if get is not None:
            x_point = int((get[1] - 430) * 480 / 3270)
            if x_point > 480:
                x_point = 480
            elif x_point < 0:
                x_point = 0
            y_point = 320 - int((get[0] - 430) * 320 / 3270)
            if y_point > 220:
                LCD.fill(LCD.WHITE)
                if x_point < 120:
                    LCD.fill_rect(0, 60, 120, 100, LCD.RED)
                    LCD.text("Button0", 20, 110, LCD.WHITE)
                elif x_point < 240:
                    LCD.fill_rect(120, 60, 120, 100, LCD.RED)
                    LCD.text("Button1", 150, 110, LCD.WHITE)
                elif x_point < 360:
                    LCD.fill_rect(240, 60, 120, 100, LCD.RED)
                    LCD.text("Button2", 270, 110, LCD.WHITE)
                else:
                    LCD.fill_rect(360, 60, 120, 100, LCD.RED)
                    LCD.text("Button3", 400, 110, LCD.WHITE)
        else:
            LCD.fill(LCD.WHITE)
            LCD.text("Button0", 20, 110, LCD.BLACK)
            LCD.text("Button1", 150, 110, LCD.BLACK)
            LCD.text("Button2", 270, 110, LCD.BLACK)
            LCD.text("Button3", 400, 110, LCD.BLACK)

        LCD.show_down()
        sleep(0.1)
