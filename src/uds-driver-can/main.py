import uds_can
import serialComm

com_port = 'COM3'
serial_baud_rate = 115200
serial_timeout = 1

if __name__ == "__main__":
  esp32 = serialComm.serialCommTester(com_port,serial_baud_rate,serial_timeout)
  newUDSTester = uds_can.UDSRequester(esp32,selfid=1,targetid=2)

  newUDSTester.sendDefaultSession()
  resp = newUDSTester.tester.recv()
  print(f"{resp}")

  newUDSTester.sendProgrammingSession()
  resp = newUDSTester.tester.recv()
  print(f"{resp}")

  newUDSTester.sendExtendedSession()
  resp = newUDSTester.tester.recv()
  print(f"{resp}")

  newUDSTester.sendSafetySystemDiagnosticSession()
  resp = newUDSTester.tester.recv()
  print(f"{resp}")