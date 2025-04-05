import uds_can
import serialComm

com_port = "COM3"
serial_baud_rate = 115200
serial_timeout = 1

if __name__ == "__main__":
    esp32 = serialComm.serialCommTester(com_port, serial_baud_rate, serial_timeout)
    newUDSTester = uds_can.UDSRequester(esp32, selfid=1, targetid=2)

    # newUDSTester.sendSession(1)
    # resp = newUDSTester.tester.recv()
    # print(f"{resp}")

    # newUDSTester.sendSession(2)
    # resp = newUDSTester.tester.recv()
    # print(f"{resp}")

    # newUDSTester.sendSession(3)
    # resp = newUDSTester.tester.recv()
    # print(f"{resp}")

    # newUDSTester.sendSession(4)
    # resp = newUDSTester.tester.recv()
    # print(f"{resp}")

    # newUDSTester.sendCodeClear()
    # resp = newUDSTester.tester.recv()
    # print(f"{resp}")

    # newUDSTester.sendECUReset(1)
    # resp = newUDSTester.tester.recv()
    # print(f"{resp}")

    # newUDSTester.sendECUReset(2)
    # resp = newUDSTester.tester.recv()
    # print(f"{resp}")

    # newUDSTester.sendECUReset(3)
    # resp = newUDSTester.tester.recv()
    # print(f"{resp}")

    # resp = newUDSTester.CodeClearProtocol()
    # print(f"{resp}")

    # resp = newUDSTester.ECUResetProtocol(1)
    # print(f"{resp}")

    # resp = newUDSTester.ECUResetProtocol(2)
    # print(f"{resp}")

    # resp = newUDSTester.ECUResetProtocol(3)
    # print(f"{resp}")

    newUDSTester.sendCustomFrame(input())
    resp = newUDSTester.tester.recv()
    print(f"{resp}")
