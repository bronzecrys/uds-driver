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

    def __init__(self, tester, selfid=0x0, targetid=0x0):
        """
        Initializes the ClassName with the given attributes.

        Args:

        """
        self.tester = tester
        self.selfid = selfid
        self.targetid = targetid

        self.DefaultSession = [0x10, 0x01]
        self.ProgrammingSession = [0x10, 0x02]
        self.ExtendedSession = [0x10, 0x03]
        self.SafetySystemDiagnosticSession = [0x10, 0x04]
        self.PositiveSessionResponse = [0x50, 0x03]
        self.NegativeSessionResponse = [0x7F, 0x10]

        self.CodeClear = [0x14]
        self.PositiveCodeClearResponse = [0x54]
        self.NegativeCodeClearResponse = [0x7F, 0x14]

        self.ECUReset_Hard = [0x11, 0x01]
        self.ECUReset_KeyOffOn = [0x11, 0x02]
        self.ECUReset_Soft = [0x11, 0x03]
        self.PositiveECUResetResponse_Hard = [0x51, 0x01]
        self.PositiveECUResetResponse_KeyOffOn = [0x51, 0x02]
        self.PositiveECUResetResponse_Soft = [0x51, 0x03]
        self.NegativeCodeClearResponse = [0x7F, 0x11]

        self.receivedResponse = ""

    def updatetargetid(self, newTargetid):
        self.targetid = newTargetid

    def receiveResponse(self):
        resp = self.tester.recv()
        self.receivedResponse = resp
        return resp

    def sendCustomFrame(self, frameData):
        data = list(bytearray.fromhex(frameData.replace(" ", "")))
        self.tester.send(self.targetid, data)

    def sendSession(self, sessionType):
        """
        Displays the information of the example.

        Returns:
            str: A string containing the name and value.
        """
        if sessionType == 1:
            self.tester.send(self.targetid, self.DefaultSession)
        elif sessionType == 2:
            self.tester.send(self.targetid, self.ProgrammingSession)
        elif sessionType == 3:
            self.tester.send(self.targetid, self.ExtendedSession)
        elif sessionType == 4:
            self.tester.send(self.targetid, self.SafetySystemDiagnosticSession)
        return

    def checkPositiveSessionResponse(self, sessionType):
        """
        Displays the information of the example.

        Returns:
            str: A string containing the name and value.
        """
        resp = self.receiveResponse()
        splitResp = resp.strip().lower().split(" ")
        if (splitResp[1] == "50") and (sessionType == splitResp[2]):
            return True
        return False

    def checkNegativeSessionResponse(self):
        """
        Displays the information of the example.

        Returns:
            str: A string containing the name and value.
        """
        resp = self.receiveResponse()
        splitResp = resp.strip().lower().split(" ")
        if (splitResp[1] == "7f") and (splitResp[1] == "10"):
            return True
        return False

    def sendCodeClear(self):
        """
        Displays the information of the example.

        Returns:
            str: A string containing the name and value.
        """
        self.tester.send(self.targetid, self.CodeClear)
        return

    def checkPositiveCodeClearResponse(self):
        """
        Displays the information of the example.

        Returns:
            str: A string containing the name and value.
        """
        resp = self.receiveResponse()
        splitResp = resp.strip().lower().split(" ")
        if splitResp[1] == "54":
            return True
        return False

    def checkNegativeCodeClearResponse(self):
        """
        Displays the information of the example.

        Returns:
            str: A string containing the name and value.
        """
        resp = self.receiveResponse()
        splitResp = resp.strip().lower().split(" ")
        if splitResp[1] == "7f" and (splitResp[1] == "14"):
            return True
        return False

    def sendECUReset(self, resetType):
        if resetType == 1:
            self.tester.send(self.targetid, self.ECUReset_Hard)
        elif resetType == 2:
            self.tester.send(self.targetid, self.ECUReset_KeyOffOn)
        elif resetType == 3:
            self.tester.send(self.targetid, self.ECUReset_Soft)
        return

    def checkPositiveECUResetResponse(self, resetType):
        """
        Displays the information of the example.

        Returns:
            str: A string containing the name and value.
        """
        resp = self.receiveResponse()
        splitResp = resp.strip().lower().split(" ")
        if (splitResp[1] == "51") and (resetType == splitResp[2]):
            return True
        return False

    def checkNegativeECUResetResponse(self):
        """
        Displays the information of the example.

        Returns:
            str: A string containing the name and value.
        """
        resp = self.receiveResponse()
        splitResp = resp.strip().lower().split(" ")
        if splitResp[1] == "7f" and (splitResp[1] == "11"):
            return True
        return False

    def CodeClearProtocol(self):
        """
        Displays the information of the example.

        Returns:
            str: A string containing the name and value.
        """
        self.sendSession(3)
        if self.checkPositiveSessionResponse("3") == False:
            return self.receivedResponse

        self.sendCodeClear()
        return self.receiveResponse()

    def ECUResetProtocol(self, resetType):
        self.sendSession(3)
        if self.checkPositiveSessionResponse("3") == False:
            return self.receivedResponse

        self.sendECUReset(resetType)
        return self.receiveResponse()


# ECU Reset
# request VID
