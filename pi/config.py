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

class DbInfo:
    def __init__(self, section):
        self.username = section['username']
        self.password = section['password']
        self.hostname = section['hostname']
        self.database = section['database']
        self.port = section['port']
