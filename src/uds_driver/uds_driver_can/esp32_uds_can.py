"""Module to send UDS messages to a CAN bus connected to the ESP32."""

import logging
import re
import time

import serial

logging.basicConfig(
    format="%(filename)s:%(levelname)s:%(asctime)s:%(message)s", level=logging.DEBUG
)


class SerialCommunication:
    """Class to communicate serially to the esp32."""

    def __init__(self, port, baudrate=115200, timeout=1):
        self.serial_com = serial.Serial(
            port, baudrate, timeout=timeout, dsrdtr=False, rtscts=False
        )
        self.serial_com.setRTS(False)
        self.serial_com.setDTR(False)
        # Clear the serial buffer.
        self.recv()

    def send(self, header, data):
        """Sends data over the serial device.

        Args:
            header (bytes): _description_
            data (bytes): _description_
        """
        logging.debug(f"Sending [{header}] with {data}.")
        byte_array = [header] + data
        self.serial_com.write(byte_array)

    def recv(self):
        """Receives incoming serial information

        Raises:
            TimeoutError: Raises timeout after a second of no communication.

        Returns:
            (str): Ascii encoded string from serial device.
        """
        timeout = time.time() + 1
        while self.serial_com.in_waiting <= 0:
            if time.time() < timeout:
                raise TimeoutError("Timed out communicating to device.")
            time.sleep(0.001)
        return self.serial_com.readline().decode("ascii")


class DataConverter:
    """Class to convert data for easy usage."""

    def convert_bytes_to_string(self, convert_bytes):
        """Method to convert a list of bytes into a string.

        Args:
            convert_bytes (list): A list of bytes.

        Returns:
            (str): A hex string in human readable format.
        """
        return " ".join(f"{byte:02X}" for byte in convert_bytes)

    def convert_string_to_bytes(self, string):
        """Method to convert a string into a list of bytes.

        Args:
            string (str): A hex string. Example: 22 f1 90

        Returns:
            (bytes): A list of bytes.
        """
        hex_string = re.split(r"[^0-9a-fA-F]+", string.strip())
        delimit = [t for t in hex_string if t]
        return [int(t.zfill(2), 16) for t in delimit]


class Esp32UdsTester:
    """Creates and sends UDS messages to the esp32 microcontroller.

    Uses a serial-CAN wrapper.

    Attributes:
      tester (obj): General object to transmit CAN message information to.
        Requires a wrapped "send" function
    """

    def __init__(self, tester, self_id=0x0, target_id=0x0):
        """Initializes the ESP32 UDS testing.

        Attributes:
            tester (obj): Wrapper for the serial communication.
            self_id (int): The identifier of the UDS tester (source ID).
            target_id (int): The identifier of the ECU or target node (destination ID).
        """
        self.tester = tester
        self.self_id = self_id
        self.target_id = target_id
        self.converter = DataConverter()

    def updatetarget_id(self, new_target_id):
        """Updates the target identification number.

        Args:
            new_target_id (int): The identifier of the ECU or target node (destination ID).
        """
        self.target_id = new_target_id

    def receive_response(self):
        """Receives the response from the serial communication device.

        Returns:
            (str): Returns a formatted hex string.
        """
        resp = self.tester.recv()
        return self.converter.convert_bytes_to_string(resp)

    def send_uds_message(self, data):
        """Sends a byte list to the target CAN bus.

        Args:
            data (str): A hex formatted string of a diagnostic request.

        Returns:
            (str): Returns a formatted hex string response.
        """
        data = self.converter.convert_string_to_bytes(data)
        self.tester.send(self.target_id, data)
        return self.receive_response()
