from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import ipaddress
import os

class QLineEditStub(QLineEdit):
    def __init__(self):
        QLineEdit.__init__(self)

    def Validate(self):
        return True, None

class QLineEditPort(QLineEdit):
    def __init__(self):
        QLineEdit.__init__(self)

    def Validate(self):
        if self.text().isdigit():
            portNum=int(self.text())
            if portNum > 0 and portNum < 65535:
                return True, None
        return False, "Wronge Port Number [" + self.text() +"]"

class QLineEditIP(QLineEdit):
    def __init__(self):
        QLineEdit.__init__(self)

    def Validate(self):
        try:
            ipaddress.ip_address(self.text())
            return True, None
        except:
            return False, "Wrong Ip Address [" + self.text() +"]"

class QLineEditFile(QLineEdit):
    def __init__(self):
        QLineEdit.__init__(self)
        self.setReadOnly(True)
        
    def Validate(self):
        print(self.text())
        if self.text() is not "":
            if os.path.exists(self.text()):
                if os.path.isfile(self.text()):
                    return True, None
        return False, "Failed to validate file [" + self.text() +"]"

