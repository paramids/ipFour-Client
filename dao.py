import json
from deviceRegistry import DeviceRegistry as deviceRegister

# This class implements a facade that retrieves the devices that are publishing into the ipfour clients,
# retirives their information and structures them into a canonical format for transamission via MQQT

class DataAccessLayer:

    def __init__(self):
        # Maintains a link the Device Registry
        # Initialize the Device Register
        self.devReg = deviceRegister()

    def getData(self):
        payload = json.dumps(
            {
                "ph": 6.2,
                "ec": 200,
                "orp": 5.4,
                "do": 20,
       })
        # TODO Polls all the devices in device Register
        for devices in self.getSubscribedDevices():
            pass
        # TODO structure the polled data into canonical format
        return payload




    def onAccumulation(self):
        # TODO interrupt client
        pass

