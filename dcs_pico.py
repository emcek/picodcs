from serial.serialutil import SerialException

from conn import SerialSender


def main(cmd: str) -> None:
    """
    Send command to Pico to act.

    :param cmd: command dict
    """
    try:
        serial_sender = SerialSender()
        serial_sender.send(cmd)
        serial_sender.close()
    except SerialException as exc:
        print(exc)


if __name__ == '__main__':
    main('show: Testing')
