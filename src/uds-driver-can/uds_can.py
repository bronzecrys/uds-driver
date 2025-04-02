class CANMessage:
  """
    Brief description of the class.

    Attributes:
        attribute1 (type): Description of attribute1.
        attribute2 (type): Description of attribute2.
  """
  def __init__(self,id=0x0,data=[0x00,0x00,0x00,0x00]):
    """
    Initializes the ClassName with the given attributes.

    Args:
        attribute1 (type): Description of attribute1.
        attribute2 (type): Description of attribute2.
    """
    self.id = id
    self.data = data
    self.length = len(data)
  def convertToByteArray(self):
    header = [self.id]
    bytearray = header + self.data
    return bytearray

class UDSRequester:
  """
    Brief description of the class.

    Attributes:
      tester CommDevice: general object to transmit CAN message information to. Requires a wrapped "send" function
      DefaultSession CANMessage: Description of attribute1.
      ProgrammingSession CANMessage: Description of attribute2.
      ExtendedSession CANMessage: Description of attribute2.
      SafetySystemDiagnosticSession CANMessage: Description of attribute2.
      PositiveSessionResponse CANMessage: Description of attribute2.
      NegativeSessionResponse CANMessage: Description of attribute2.
      CodeClear CANMessage: Description of attribute2.
      PositiveCodeClearResponse CANMessage: Description of attribute2.
      NegativeCodeClearResponse CANMessage: Description of attribute2.
  """
  def __init__(self,tester,selfid=0x0,targetid=0x0):
    """
    Initializes the ClassName with the given attributes.

    Args:
    
    """
    self.tester=tester

    self.DefaultSession = CANMessage(targetid,[0x10,0x01])
    self.ProgrammingSession = CANMessage(targetid,[0x10,0x02])
    self.ExtendedSession = CANMessage(targetid,[0x10,0x03])
    self.SafetySystemDiagnosticSession = CANMessage(targetid,[0x10,0x04])
    self.PositiveSessionResponse = CANMessage(selfid,[0x50,0x03])
    self.NegativeSessionResponse = CANMessage(selfid,[0x7F,0x10])

    self.CodeClear = CANMessage(targetid,[0x14,0xFF,0xFF,0xFF])
    self.PositiveCodeClearResponse = CANMessage(selfid,[0x54])
    self.NegativeCodeClearResponse = CANMessage(selfid,[0x7F,0x14])

  def sendDefaultSession(self):
    """
    Displays the information of the example.

    Returns:
        str: A string containing the name and value.
    """
    self.tester.send(self.DefaultSession.convertToByteArray())
    return
  def sendProgrammingSession(self):
    """
    Displays the information of the example.

    Returns:
        str: A string containing the name and value.
    """
    self.tester.send(self.ProgrammingSession.convertToByteArray())
    return
  def sendExtendedSession(self):
    """
    Displays the information of the example.

    Returns:
        str: A string containing the name and value.
    """
    self.tester.send(self.ExtendedSession.convertToByteArray())
    return
  def sendSafetySystemDiagnosticSession(self):
    """
    Displays the information of the example.

    Returns:
        str: A string containing the name and value.
    """
    self.tester.send(self.SafetySystemDiagnosticSession.convertToByteArray())
    return
  def checkPositiveSessionResponse(self):
    """
    Displays the information of the example.

    Returns:
        str: A string containing the name and value.
    """
    return False
  def checkNegativeSessionResponse(self):
    """
    Displays the information of the example.

    Returns:
        str: A string containing the name and value.
    """
    return False
  
  def sendCodeClear(self):
    """
    Displays the information of the example.

    Returns:
        str: A string containing the name and value.
    """
    self.tester.send(self.CodeClear.convertToByteArray())
    return
  def checkPositiveCodeClearResponse(self):
    """
    Displays the information of the example.

    Returns:
        str: A string containing the name and value.
    """
    return False
  def checkNegativeCodeClearResponse(self):
    """
    Displays the information of the example.

    Returns:
        str: A string containing the name and value.
    """
    return False

  def CodeClearProtocol(self):
    """
    Displays the information of the example.

    Returns:
        str: A string containing the name and value.
    """
    self.sendExtendedSession()
    if(self.checkPositiveSessionResponse() == False):
      return -1
    self.sendCodeClear()
    if(self.checkPositiveCodeClearResponse() == False):
      return -1

  