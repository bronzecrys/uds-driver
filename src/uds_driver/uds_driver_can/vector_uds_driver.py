"""Class to communicate to a Vector Bus with Normal 11 bit addressing."""

import logging
import re
import threading
import time

import can
import isotp

logging.basicConfig(
    format="%(filename)s:%(levelname)s:%(asctime)s:%(message)s", level=logging.DEBUG
)

logging.getLogger("can").setLevel(logging.ERROR)
logging.getLogger("can.interfaces.vector").setLevel(logging.ERROR)
logging.getLogger("can.vector").setLevel(logging.ERROR)
logging.getLogger("isotp").setLevel(logging.ERROR)
logging.getLogger("isotp.protocol").setLevel(logging.ERROR)


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


class CanMessenger:
    """Method to generate CAN messages."""

    def __init__(self, bus):
        """
        Manages CAN messages with dynamic payload updates.

        Args:
            bus (obj): A bus object.
        """
        self.converter = DataConverter()
        self.bus = bus
        self.tasks = {}
        self.lock = threading.Lock()

    def add_periodic_message(self, arb_id, data, period=1.0, is_extended_id=False):
        """Adds and starts a new periodic message.

        Args:
            arb_id (int): CAN arbitration ID.
            data (list): List of up to 8 integers (0–255) representing the payload.
            period (float): Send interval in seconds.
            is_extended_id (bool): True if using 29-bit extended ID.
        """
        send_data = self.converter.convert_string_to_bytes(data)
        with self.lock:
            msg = can.Message(
                arbitration_id=int(arb_id, 16),
                data=(send_data + [0x00] * 8)[:8],
                is_extended_id=is_extended_id,
            )
            task = self.bus.send_periodic(msg, period=period)
            self.tasks[arb_id] = {"message": msg, "task": task}
            send_time = time.time()
            logging.debug(f"[{send_time}]   [{arb_id}]: {data}")

    def update_payload(self, arb_id, data):
        """Updates the payload of a running periodic message.

        Args:
            arb_id (int): Arbitration ID of the message to update.
            data (list): New data (up to 8 bytes).
        """
        update_data = self.converter.convert_string_to_bytes(data)
        with self.lock:
            if arb_id in self.tasks:
                msg = self.tasks[arb_id]["message"]
                msg.data[:] = (update_data + [0x00] * 8)[:8]
                logging.debug(f"Updated 0x{arb_id} payload to: {msg.data}")
            else:
                logging.debug(f"No periodic message found for 0x{arb_id}")

    def stop_message(self, arb_id):
        """Stops a specific periodic message.

        Args:
            arb_id (int): Arbitration ID of the message to stop.
        """
        with self.lock:
            if arb_id in self.tasks:
                self.tasks[arb_id]["task"].stop()
                del self.tasks[arb_id]
                logging.debug(f"Stopped periodic msg on 0x{arb_id}")

    def stop_all(self):
        """Stops all periodic messages."""
        with self.lock:
            for entry in self.tasks.values():
                entry["task"].stop()
            self.tasks.clear()
            logging.debug("Stopped all periodic messages.")

    def send_single_message(self, arb_id, data, is_extended_id=False):
        """Sends a spontaneous CAN message to the arbitration ID.

        Args:
            arb_id (str): A hex string representation of the arbitration id.
            data (str): A hex string representation of the message values to send.
            is_extended_id (bool, optional): If 11 bit CAN is extended. Defaults to False.
        """
        send_data = self.converter.convert_string_to_bytes(data)
        msg = can.Message(
            arbitration_id=int(arb_id, 16),
            data=(send_data + [0x00] * 8)[:8],
            is_extended_id=is_extended_id,
        )
        self.bus.send(msg)


class VectorUdsManager:
    """Class to send UDS commands to an ECU serially through a Vector interface."""

    def __init__(self, serial, channel=0, bitrate=500000):
        self.interface = "vector"
        self.channel = channel
        self.bitrate = bitrate
        self.serial = serial
        self.bus = None
        self.converter = DataConverter()

    def connect(self):
        """Connects to a vector CAN bus.

        Returns:
            (obj): Returns a Vector CAN bus object.
        """
        self.bus = can.interface.Bus(
            interface=self.interface,
            bitrate=self.bitrate,
            channel=self.channel,
            serial=self.serial,
        )
        return self.bus

    def set_stack(self, tx, rx, params):
        """Sets the ISO transfer protocol stack.

        Args:
            tx (str): The transmission arbitration id.
            rx (str): The reception arbitration id.
            params (dict): A dictionary of parameter values.

        Returns:
            (obj): Transfer protocol object.
        """
        address = isotp.Address(
            isotp.AddressingMode.Normal_11bits,
            txid=int(tx, 16),
            rxid=int(rx, 16),
        )

        stack = isotp.CanStack(bus=self.bus, address=address, params=params)

        # Flush any leftover frames
        _ = stack.recv()
        return stack

    def send_uds_message(self, message, tx, rx, params=None, timeout=2.0):
        """Sends a diagnostic message and wait for the response.

        Args:
            message (str): Hex value representation of the data to send on the frame.
            tx (str): Hex value representation of the transmission arbitration id.
            rx (str): Hex value representation of the reception arbitration id.
            params (dict, optional): Additional values to send with the TP stack. Defaults to None.
            timeout (float, optional): Hard timeout for diagnostics. Defaults to 2.0.

        Returns:
            response (str): Returns the string response from the diagnostic request.
        """
        if params is None:
            params = {"tx_padding": 0x00}

        # Send raw UDS request
        msg = self.converter.convert_string_to_bytes(message)
        stack = self.set_stack(tx, rx, params)
        send_time = time.time()
        stack.send(msg)

        ref_timeout = time.time() + timeout
        response = None

        while time.time() < ref_timeout:
            stack.process()
            if stack.available():
                response = stack.recv()
                if len(response) >= 3 and response[0] == 0x7F and response[2] == 0x78:
                    response = None
                else:
                    break
            time.sleep(0.01)

        if response:
            response_time = time.time()
            logging.debug(f"[{send_time}]   [{tx}]: {message}")
            logging.debug(
                f"{response_time}] [{rx}]: {self.converter.convert_bytes_to_string(response)}"
            )
            return self.converter.convert_bytes_to_string(response)
        else:
            logging.error("Timed out waiting for response.")
            return False


if __name__ == "__main__":
    # Example usage
    uds = VectorUdsManager(serial=1234567)
    bus = uds.connect()
    manager = CanMessenger(bus)
    # You can then use the methods as documented.
