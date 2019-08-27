
# This should be a static class


class DeviceRegistry(object):

    __instance = None


    @staticmethod
    def getInstance():
        if DeviceRegistry.__instance == None:
            DeviceRegistry()
        else:
            return DeviceRegistry.__instance

    def __init__(self):
        if DeviceRegistry.__instance != None:
            raise Exception("This class is a Singleton..")
        else:
            DeviceRegistry.__instance = self
        self.deviceRegister = []

    # This methods listens on to different devices. This methods takes in device info contaning device information and
    # schema of the data that is being sent.
    def registerDevice(self,  deviceinfo):
        self.deviceRegister.append(deviceinfo.name, deviceinfo)

    def removeDevice(self, deviceinfo):
        self.deviceRegister[deviceinfo.name] = None

    @getattr()
    def getDeviceRegister(self):
        return self.deviceRegister

    def getDeviceInfo(self, devicename):
        return self.devReg.deviceRegister

    def getSubscribedDevices(self):
        return self.devReg


class DeviceInfo(object):
    def __init__(self):
        self.name = None
        self.protocol = None
        self.dataSchema = None