"""
Peer 2 peer local network

Based on the socket library
"""
from ast import arg
import socket
import struct
import time
import threading
import traceback

import config

class Peer():
    """
    Implements the core functionality that might be used by a peer in a P2P network.
    """

    def __init__(self, maxnodes_p, serverport_p, id_p, serverhost_p):
        """
        Initialize peer node
        - maxnodes     : Number of nodes (if set to 0 -> unlimited nodes) 
        - serverport   : listen on a giver port
        - id           : id of the node
        - serverhost   : host address
        """
        self.maxnodes = maxnodes_p
        self.serverport = serverport_p
        self.serverhost = serverhost_p

        self.nodes = {}       # Used to map nodes (host, port)
        self.handlers = {}    # Used to map handlers
        self.router = None

        self.shutdown = False # Used to stop the main loop

        self.lock = threading.Lock() # Ensure proprer access to node list (Because threads manage the list)
        
        if id_p:
            self.id = id_p
        else:
            self.id = '%s:%d' % (self.serverhost, self.serverport)

    def createServerSocket(self, port_p, backlog_p=5):
        """
        Create an INET (IPv4), STREAMing socket.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        sock.bind(('',port_p)) #Accessed by anyone
        sock.listen(backlog_p)
        return sock
    
    def removeDeadNodes(self):
        """
        Remove dead nodes
        Does not check if new born nodes are available
        """
        deadNodes = []
        for node in self.nodes:
            try:
                connected = False
                host, port = self.nodes[node]
                nodeConn = NodeConnection(node, host, port)
                nodeConn.sendData('PING', '')
                connected = True
            except:
                deadNodes.append(node)
            if connected:
                nodeConn.close()

        self.lock.acquire()
        for node in deadNodes:
            if node in self.nodes:
                del self.nodes[node]
        self.lock.release()
    
    def handleNodes(self, clientstock_p):
        """
        Handle new connections
        """

        print("Connected to {0}").format(clientstock_p)
        
        host, port = clientstock_p.getpeername()
        nodeCon = NodeConnection(None, host, port, clientstock_p)
        
        try:
            msgtype, msgdata = nodeCon.recvdata()
            if msgtype: msgtype = msgtype.upper()
            if msgtype not in self.handlers:
                print("Not handled: %s: %ss", msgtype, msgdata)
            else:
                print("Hqndling node msg: %s: %ss", msgtype, msgdata)
            self.handlers[ msgtype ]( nodeCon, msgdata )

        except KeyboardInterrupt:
            raise
        
        nodeCon.close()


    
    def main(self):
        sock = self.createServerSocket(self.serverport)
        sock.settimeout(2)
        print("Node started")
        
        while not self.shutdown:
            try:
                print("Listening for connections")
                clientsock, clientaddr = sock.accept()
                clientsock.settimeout(None)

                thread = threading.Thread(target=self.handleNodes, args=clientsock)
                thread.start()
                
            except:
                print("Stopping node {}").format(self.id)
                self.shutdown = True

        sock.close()


    
    @property
    def setID(self, id_p):
        self.id = id_p
    
    @property
    def getID(self):
        return self.id
    
    @property
    def setServerPort(self, serverport_p):
        self.serverport = serverport_p
    
    @property
    def getServerPort(self):
        return self.serverport
    
    @property
    def setServerHost(self, serverhost_p):
        self.serverhost = serverhost_p
    
    @property
    def getServerHost(self):
        return self.serverhost
    
    @property
    def setNodes(self, nodes_p):
        self.nodes = nodes_p
    
    @property
    def addNode(self, nodeid_p , host_p, port_p):
        if nodeid_p not in self.nodes and (self.maxnodes == 0 or len(self.nodes)<self.maxnodes):
            self.nodes [nodeid_p] = (host_p, port_p)
            return True
        else:
            return False
    
    @property
    def removeNodes(self, nodeid_p):
        if nodeid_p in self.nodes:
            del self.nodes[nodeid_p]
            return True
        else:
            print("Given node not found")
            return False

    @property
    def getNodes(self):
        return self.nodes
    
    @property
    def getNode(self, nodeid_p):
        assert nodeid_p in self.nodes
        return self.nodes[nodeid_p]
    
    @property
    def maxNodesReached(self):
        assert self.maxnodes == 0 or len(self.nodes)<self.maxnodes
        return self.maxnodes == 0 or len(self.nodes)<self.maxnodes
    
    @property
    def addRouter(self, router_p):
        self.router = router_p
    
    @property
    def getRouter(self):
        return self.router
    
    @property
    def addHandler(self, msgType_p, handler_p):
        assert handler_p in self.handlers
        self.handlers[msgType_p] = handler_p
    
    @property
    def getHandler(self, msgType_p):
        return self.handlers[msgType_p]
    
    @property
    def getHandlers(self):
        return self.handlers

    
class NodeConnection():
    """
    Connect two nodes as a peer to peer connection
    """
    def __init__(self, nodeid_p, host_p, port_p, sock_p=None):

        self.id = nodeid_p

        if not sock_p:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host_p, port_p))
        else:
            self.sock = sock_p

        self.sd = self.s.makerfile('rw',0)

    def __makemsg(self, msgtype_p, msgdata_p):
        msglen = len(msgdata_p)
        msg = struct.pack("!sL%ds" % msglen, msgtype_p, msgdata_p)
        return msg

    def sendData(self, msgtype_p, msgdata_p):
        """
        senddata( message type, message data ) -> boolean status

        Send a message through a peer connection. Returns True on success
        or False if there was an error.
        """

        try:
            msg = self.__makemsg(msgtype_p, msgdata_p)
            self.sd.write( msg )
            self.sd.flush()
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
            return False
        return True


    def receiveData(self):
        """
        recvdata() -> (msgtype, msgdata)

        Receive a message from a peer connection. Returns (None, None)
        if there was any error.
        """
        try:
            msgtype = self.sd.read( 4 )
            if not msgtype: return (None, None)
            
            lenstr = self.sd.read( 4 )
            msglen = int(struct.unpack( "!L", lenstr )[0])
            msg = ""

            while len(msg) != msglen:
                data = self.sd.read( min(2048, msglen - len(msg)) )
                if not len(data):
                    break
                msg += data

            if len(msg) != msglen:
                return (None, None)

        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
            return (None, None)

        return ( msgtype, msg )

    def close(self):
        self.s.close()
        self.s = None
        self.sd = None
    
