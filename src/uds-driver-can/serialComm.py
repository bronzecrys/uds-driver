import serial
import time



class serialCommTester:
  def __init__(self,port, baudrate=115200, timeout=1):
    serialComm = serial.Serial(port, baudrate, timeout=timeout,dsrdtr=False,rtscts=False)
    serialComm.setRTS(False)
    serialComm.setDTR(False)
    self.serialComm = serialComm
    # clear the serial buffer in case initializing the connection resets the connected board & it begins to write to the serial connection
    resp = ''
    while resp != 'timeout':
      resp = self.recv()
      print(resp)

  def send(self,byteArray):
    self.serialComm.write(byteArray)

  def recv(self):
    timeout = 1000
    # wait until their are bytes available, use timeout to break and avoid infinite loop and
    while self.serialComm.in_waiting <= 0:
      timeout = timeout - 1
      if timeout == 0:
        return "timeout"
      time.sleep(.001)
    return self.serialComm.readline().decode('ascii')