import serial


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
        line = f'{text}\n'
        self.serial.write(line.encode('UTF8'))

    def close(self):
        """Exit."""
        self.serial.close()
