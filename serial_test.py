import serial
from serial.serialutil import SerialException
from time import sleep


# modified from https://blog.rareschool.com/2021/01/controlling-raspberry-pi-pico-using.html
class SerialSender:
    TERMINATOR = '\n'.encode('UTF8')

    def __init__(self, device='COM3', baud=115200, timeout=1):
        self.serial = serial.Serial(device, baud, timeout=timeout)

    def receive(self) -> str:
        line = self.serial.read_until(self.TERMINATOR)
        return line.decode('UTF8').strip()

    def send(self, text: str):
        line = '%s\n' % text
        self.serial.write(line.encode('UTF8'))

    def close(self):
        self.serial.close()


# https://stackoverflow.com/a/66037406
async def get_media_info():
    info_dict = {'title': 'Song 2'}
    return info_dict


if __name__ == '__main__':
    previous_media_info = None
    while True:
        current_media_info = get_media_info()

        if current_media_info != previous_media_info and current_media_info is None:
            print(current_media_info['title'])
            previous_media_info = current_media_info
            sleep(1)

            # recreate the serial each time to allow handling disconnection
            try:
                serial_sender = SerialSender()
                serial_sender.send(current_media_info['title'])
                serial_sender.close()
            except SerialException:
                pass
