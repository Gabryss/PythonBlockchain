"""
Agent class

Each agent is based on a process that use only pipe to communicate.
When agents are initialized all of basic attributes are stored in the class

A time delay is used to fake inlunar environment.
"""

from concurrent.futures import process
import multiprocessing
from queue import Empty
import time



class Agent():

    def __init__(self, data_p, pipe_p, name_p):
        self.name = name_p
        self.pipe = pipe_p
        self.data = [data_p]
        self.running = True

    def sendData(self,pipe,data):
        print('Process {0} is sending {1}'.format(self.name, data))
        pipe.send(data)
        self.data.pop()
        return 1

    def receiveData(self, pipe):
        print("Process {0} wait to receive data".format(self.name))
        received_data = pipe.recv()
        self.data.append(received_data)
        print("Process {0} received data : {1}".format(self.name, received_data))
        return 1
    
    def closeAgent(self):
        #Not working somehow
        self.agent.terminate()

    def startAgent(self):
        self.agent = multiprocessing.Process(target=self.runAgent, name=self.name)
        self.pid = self.agent.pid
        self.agent.start()

    def runAgent(self):
        while True:
            if len(self.data) == 0:
                print("Closing")
                break
            for data in self.data:
                print("The sending data is {0}".format(data))
                self.sendData(self.pipe,data)
            self.receiveData(self.pipe)
            print(self.agent.pid)
            print(self.pid)
            time.sleep(0.5)