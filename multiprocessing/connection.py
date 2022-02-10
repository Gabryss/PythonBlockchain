"""
Connection class

Used to return a pipe connection between agents
"""

import multiprocessing

class Connection():

    def __init__(self, name_p):
        self.name = name_p


    def createPipe(self, duplex_p=True):
        self.entrance1, self.entrance2 = multiprocessing.Pipe(duplex=duplex_p)