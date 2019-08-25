from random import randint
from time import clock

import paho.mqtt.client as mqtt
from dao import DataAccessLayer as acc

# =========================================================================================================
# TRANSITIONS


class Transition(object):
    def __init__(self, toState):
        self.toState = toState

    def Execute(self):
        print "Transitioning..."


# =========================================================================================================
# OBSERVERS

class Event(object):

    def __init__(self, FSM):
        self.FSM = FSM



class DataReadySubject(object):

    __instance = None

    @staticmethod
    def getInstance():
        if DataReadySubject.__instance == None:
            DataReadySubject()
        return DataReadySubject.__instance

    def __init__(self):
        if DataReadySubject.__instance != None:
            raise Exception("This class is a Singleton..")
        else:
            DataReadySubject.__instance = self

        self.observers = []

    def bind_to(self, callback):
        print('Bound')
        self.observers.append(callback)

    def notify(self):
        for callback in self.observers:
            print ('Announcing Data Ready Change')
            callback()

class ConnectedSubject(object):

    __instance = None

    @staticmethod
    def getInstance():
        if ConnectedSubject.__instance is None:
            ConnectedSubject()
        return ConnectedSubject.__instance

    def __init__(self):
        if ConnectedSubject.__instance != None:
            raise Exception("This is a Singleton..")
        else:
            ConnectedSubject.__instance = self
        self.observers = []

    def bind_to(self, callback):
        print('Bound')
        self.observers.append(callback)

    def notify(self):
        for callback in self.observers:
            print ('Announcing Establishment of Connection with CLoud ')
            callback()


class DataReadyEvent(Event):
    toState = "AccumulateState"
    fromState = "ConnectedState"

    def __init__(self, subject, FSM):
        super(DataReadyEvent,self).__init__(FSM)
        self.subject = subject
        self.subject.bind_to(self.onEvent)


    def onEvent(self):
        # TODO Do the state transition from Connected state to Accumulate State
        print('Reached Data Ready Event')
        if self.FSM.curState == self.FSM.states["ConnectedState"]:
            self.FSM.ToTransition("DataReadyEvent")


class ConnectedEvent(Event):
    toState = "ConnectedState"
    fromState = "InitState"

    def __init__(self, subject, FSM):
        super(ConnectedEvent, self).__init__(FSM)
        self.subject = subject
        self.subject.bind_to(self.onEvent)

    def onEvent(self):
        # TODO Do the state transition from Intit state to Connected State
        print('Reached Connection Event')
        if self.FSM.curState == self.FSM.states["InitState"]:
            self.FSM.ToTransition("ConnectedEvent")

##=========================================================================================================
##STATES


class State(object):
    def __init__(self, FSM):
        self.FSM = FSM
        self.timer = 0
        self.startTime = 0
        self.mqqtc = mqtt.Client()

    def Enter(self):
        self.timer = randint(0,5)
        self.startTime = int(clock())

    def Execute(self):
        pass

    def Exit(self):
            pass


class InitState(State):
    def __init__(self, FSM):
        super(InitState, self).__init__(FSM)

    def Enter(self):
        print("Entering InitState...")
        super(InitState, self).Enter()

    def Execute(self):
        # TODO Connect to IpFour Communication service via MQTT
        try:
            self.mqqtc.connect("cloud.ipfour.net", 1883)
            self.mqqtc.loop_start()
            if (self.startTime + self.timer <= clock()):
                self.FSM.ToTransition("ConnectedEvent")
        except:
            print('Error Occured when connecting to ipfour server')
            ConnectedSubject.getInstance().notify()




class ConnectedState(State):
    def __init__(self, FSM):
        super(ConnectedState, self).__init__(FSM)

    def Enter(self):
        print("Entering ConnectedState...")
        super(ConnectedState, self).Enter()

    def Execute(self):
        # Implement the work that has to be done in this state

        if(self.startTime + self.timer <= clock()):
            # Transition from the current state is implemented here
            #if randint(0.2)%2:
                #self.FSM.ToTransition("NextState")
            pass


class PublishDataState(State):
    def __init__(self, FSM):
        super(PublishDataState, self).__init__(FSM)

    def Enter(self):
        print("Preparing to Enter...")
        super(PublishDataState, self).Enter()

    def Execute(self):
        # publish Data block
        topic = "ipfour/v1/dcx/myToken/json"
        payload = acc.getData()
        self.mqqtc.publish(topic=topic, payload=payload)
        if(self.startTime + self.timer <= clock()):
            self.FSM.ToTransition("ConnectedState")


class AccumulateState(State):
    def __init__(self, FSM):
        super(AccumulateState, self).__init__(FSM)

    def Enter(self):
        print("Entering AccumulateState...")
        super(AccumulateState, self).Enter()

    def Execute(self):
        # Implement the work that has to be done in this state

        if(self.startTime + self.timer <= clock()):
            # Transition from the current state is implemented here
            pass


class ScanDevicesState(State):
    def __init__(self, FSM):
        super(ScanDevicesState, self).__init__(FSM)

    def Enter(self):
        print("Preparing to Enter...")
        super(ScanDevicesState, self).Enter()

    def Execute(self):
        # Implement the work that has to be done in this state

        if(self.startTime + self.timer <= clock()):
            # Transition from the current state is implemented here
            if randint(0.2)%2:
                self.FSM.ToTransition("NextState")


class ListeningState(State):
    def __init__(self, FSM):
        super(ListeningState, self).__init__(FSM)

    def Enter(self):
        print("Preparing to Enter...")
        super(ListeningState, self).Enter()

    def Execute(self):
        # Implement the work that has to be done in this state

        if(self.startTime + self.timer <= clock()):
            # Transition from the current state is implemented here
            if randint(0.2)%2:
                self.FSM.ToTransition("NextState")

#=========================================================================================================
## FINTITE STATE MACHINES

class FSM(object):
    def __init__(self, character):
        self.char = character
        self.states = {}
        self.transitions = {}
        self.curState = None
        self.prevState = None
        self.trans = None
        # TODO Register to External Event Subjects


    def AddTransition(self, transName, transition):
        self.transitions[transName] = transition

    def ToTransition(self, totrans):
        print ('Transition Triggered')
        self.trans = self.transitions[totrans]

    def AddState(self, stateName, state):
        self.states[stateName] = state

    def SetState(self, stateName):
        self.prevState = self.curState
        self.curState= self.states[stateName]

    def Execute(self):
        if self.trans:
            self.curState.Exit()
            # self.trans.Execute()
            self.SetState(self.trans.toState)
            self.curState.Enter()
            self.trans = None
        self.curState.Execute()

#=========================================================================================================
## IMPLEMENTATION


Char = type("Char", (object,), {})


class IpFourClient(Char):

    def __init__(self):
            self.FSM = FSM(self)

            # STATES
            self.FSM.AddState("InitState", InitState(self.FSM))
            self.FSM.AddState("ConnectedState", ConnectedState(self.FSM))
            self.FSM.AddState("PublishedState", PublishDataState(self.FSM))
            self.FSM.AddState("AccumulateState", AccumulateState(self.FSM))

            #EVENTS
            self.subject1 = DataReadySubject()
            self.subject2 = ConnectedSubject()
            self.FSM.AddTransition("DataReadyEvent", DataReadyEvent(self.subject1, self.FSM))
            self.FSM.AddTransition("ConnectedEvent", ConnectedEvent(self.subject2, self.FSM))


            self.FSM.SetState("InitState")
    def Execute(self):
        self.FSM.Execute()


if __name__=='__main__':
    c = IpFourClient()
    while(True):
        startTime = clock()
        timeInterval = 1
        while (startTime + timeInterval > clock()):
            pass
        c.Execute()
        c.subject1.notify()
