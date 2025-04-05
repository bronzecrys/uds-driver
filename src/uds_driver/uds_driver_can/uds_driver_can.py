"""Module to communicate to multiple devices."""

import time

from esp32_uds_can import Esp32UdsTester, SerialCommunication
from vector_uds_driver import CanMessenger, VectorUdsManager

COM_PORT = "COM3"
BAUD_RATE = 115200
TIMEOUT = 1
VECTOR_ID = 1234567
NM_MESSAGE_ID = 123
NM_MESSAGE_FRAME = "11 22 33 44"
TX_ARB = "7E0"
RX_ARB = "7E8"


class UdsDriver:
    """Driver to send generic UDS requests to a CAN bus"""

    def __init__(self, interface, com_port=None, baud=None, timeout=None, serial=None):
        self.com_port = com_port
        self.baud = baud
        self.timeout = timeout
        self.can_messenger = None
        self.diagnostic_messenger = None
        if interface == "vector":
            self.diagnostic_messenger = VectorUdsManager(serial=serial)
            bus = self.diagnostic_messenger.connect()
            self.can_messenger = CanMessenger(bus)
        else:
            self.can_messenger = SerialCommunication(
                self.com_port, self.baud, self.timeout
            )
            self.diagnostic_messenger = Esp32UdsTester(
                self.can_messenger, selfid=1, targetid=2
            )

    def send_default_session(self, tx=None, rx=None):
        """Sends a default session request for UDS standard ISO-14229-1

        0x10 - Service Identifier
        0x01 - Session Identifier

        Args:
            tx (str, optional): Transmission ID for the transport protocol. Defaults to None.
            rx (str, optional): Reception ID for the transport protocol. Defaults to None.

        Returns:
            (str): Returns formatted hex string diagnostic response.
        """
        data = "10 01"
        if rx is None and tx is None:
            return self.diagnostic_messenger.send_uds_message(data)
        return self.diagnostic_messenger.send_uds_message(data, tx, rx)

    def send_programming_session(self, tx=None, rx=None):
        """Sends a programming session request for UDS standard ISO-14229-1

        0x10 - Service Identifier
        0x02 - Session Identifier

        Args:
            tx (str, optional): Transmission ID for the transport protocol. Defaults to None.
            rx (str, optional): Reception ID for the transport protocol. Defaults to None.

        Returns:
            (str): Returns formatted hex string diagnostic response.
        """
        data = "10 02"
        if rx is None and tx is None:
            return self.diagnostic_messenger.send_uds_message(data)
        return self.diagnostic_messenger.send_uds_message(data, tx, rx)

    def send_extended_session(self, tx=None, rx=None):
        """Sends a extended session request for UDS standard ISO-14229-1

        0x10 - Service Identifier
        0x03 - Session Identifier

        Args:
            tx (str, optional): Transmission ID for the transport protocol. Defaults to None.
            rx (str, optional): Reception ID for the transport protocol. Defaults to None.

        Returns:
            (str): Returns formatted hex string diagnostic response.
        """
        data = "10 03"
        if rx is None and tx is None:
            return self.diagnostic_messenger.send_uds_message(data)
        return self.diagnostic_messenger.send_uds_message(data, tx, rx)

    def check_session_request(self, tx=None, rx=None):
        """Sends a check session request for UDS standard ISO-14229-1

        0x22 - Service Identifier
        0xF1 0x86 - Read Diagnostic Identifier

        Args:
            tx (str, optional): Transmission ID for the transport protocol. Defaults to None.
            rx (str, optional): Reception ID for the transport protocol. Defaults to None.

        Returns:
            (str): Returns formatted hex string diagnostic response.
        """
        data = "22 F1 86"
        if rx is None and tx is None:
            return self.diagnostic_messenger.send_uds_message(data)
        return self.diagnostic_messenger.send_uds_message(data, tx, rx)

    def send_clear_dtc(self, tx=None, rx=None):
        """Sends a fault memory request for UDS standard ISO-14229-1

        0x14 - Service Identifier
        0xFF 0xFF 0xFF - Clear request

        Args:
            tx (str, optional): Transmission ID for the transport protocol. Defaults to None.
            rx (str, optional): Reception ID for the transport protocol. Defaults to None.

        Returns:
            (str): Returns formatted hex string diagnostic response.
        """
        data = "14 FF FF FF"
        if rx is None and tx is None:
            return self.diagnostic_messenger.send_uds_message(data)
        return self.diagnostic_messenger.send_uds_message(data, tx, rx)

    def send_ecu_reset(self, tx=None, rx=None):
        """Sends a ECU reset request for UDS standard ISO-14229-1

        0x11 - Service Identifier
        0x01 - Non-silent request identifier

        Args:
            tx (str, optional): Transmission ID for the transport protocol. Defaults to None.
            rx (str, optional): Reception ID for the transport protocol. Defaults to None.

        Returns:
            (str): Returns formatted hex string diagnostic response.
        """
        data = "11 01"
        if rx is None and tx is None:
            return self.diagnostic_messenger.send_uds_message(data)
        return self.diagnostic_messenger.send_uds_message(data, tx, rx)


if __name__ == "__main__":
    diagnostic_message = UdsDriver("vector", serial=VECTOR_ID)
    diagnostic_message.can_messenger.add_periodic_message(
        NM_MESSAGE_ID, NM_MESSAGE_FRAME, period=1
    )
    diagnostic_message.send_default_session(TX_ARB, RX_ARB)
    diagnostic_message.check_session_request(TX_ARB, RX_ARB)
    time.sleep(2)
    diagnostic_message.send_programming_session(TX_ARB, RX_ARB)
    diagnostic_message.check_session_request(TX_ARB, RX_ARB)
    time.sleep(2)
    diagnostic_message.send_extended_session(TX_ARB, RX_ARB)
    diagnostic_message.check_session_request(TX_ARB, RX_ARB)
    time.sleep(2)
    diagnostic_message.send_clear_dtc(TX_ARB, RX_ARB)
    diagnostic_message.send_ecu_reset(TX_ARB, RX_ARB)
    time.sleep(5)
    diagnostic_message.check_session_request(TX_ARB, RX_ARB)
    time.sleep(10)
