from shutil import copyfile
import os.path
from configobj import ConfigObj

class Configuration:
    def __init__(self):
        path = "../poppi.conf"
        if not os.path.exists(path):
            copyfile("poppi.conf", path)
        config = ConfigObj(path)
        self.db = DbInfo(config['MySQL'])
        self.rfid = RfidInfo(config['RFID'])
        self.popMachine = PopMachineInfo(config['PopMachine'])
        self.coinAcceptor = CoinAcceptorInfo(config['CoinAcceptor'])
        self.coinMap = CoinMapInfo(config['CoinMap'])
        self.web = WebInfo(config['Web'])

class DbInfo:
    def __init__(self, section):
        self.username = section['username']
        self.password = section['password']
        self.hostname = section['hostname']
        self.database = section['database']
        self.port = section['port']

class RfidInfo:
    def __init__(self, section):
        self.serialPort = section['serialPort']

class PopMachineInfo:
    def __init__(self, section):
        self.relayPin = int(section['relayPin'])

class CoinAcceptorInfo:
    def __init__(self, section):
        self.inhibitPin = int(section['inhibitPin'])
        self.serialPort = section['serialPort']

class WebInfo:
    def __init__(self, section):
        self.port = int(section['port'])
        self.bindAddress = section['bindAddress']

class CoinMapInfo:
    def __init__(self, section):
        self.__section = section

    def getCentValue(self, numericValue):
        asStr = "0x%02X" % numericValue
        return int(self.__section[asStr])
