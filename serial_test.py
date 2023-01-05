import serial
from serial.serialutil import SerialException
from time import sleep


# modified from https://blog.rareschool.com/2021/01/controlling-raspberry-pi-pico-using.html
class SerialSender:
    """Serial handler."""
    TERMINATOR = '\n'.encode('UTF8')

    def __init__(self, device='COM3', baud=115200, timeout=1):
        """
        Create.

        :param device:
        :param baud:
        :param timeout:
        """
        self.serial = serial.Serial(device, baud, timeout=timeout)

    def receive(self) -> str:
        """
        Receive.

        :return:
        """
        line = self.serial.read_until(self.TERMINATOR)
        return line.decode('UTF8').strip()

    def send(self, text: str):
        """
        Send.

        :param text:
        """
        line = '%s\n' % text
        self.serial.write(line.encode('UTF8'))

    def close(self):
        """Exit."""
        self.serial.close()


if __name__ == '__main__':
    previous_media_info = None
    while True:
        current_media_info = {'title': 'Song 2'}

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
