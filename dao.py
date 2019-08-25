import json

DEVICE_REGISTRY = {}


class DataAccessLayer:

    def __init__(self):
        DEVICE_REGISTRY = {}
        pass

    def getData(self):
        # TODO assemble data payload from registered devices.
        payload = json.dumps(
            {
                "ph": 6.2,
                "ec": 200,
                "orp": 5.4,
                "do": 20,
       })
        return payload

    def onAccumulation(self):
        # TODO interrupt client
        pass

