from cgi import test
import logging
import multiprocessing
import time

import agent
import connection

def basic_func(item):
    proc_name = multiprocessing.current_process().name
    print('This is a process with the id : {0}'.format(proc_name))
    print(item)
    time.sleep(2)
    

def double(number):
    return number*number

def create_process(n, function, items = None):
    
    #Create process
    for i in range(n):
        proc = multiprocessing.Process(target=function, args=(items[i%3],))
        process.append(proc)
        proc.start()

    #Tell them to wait for instructions
    for proc in process:
        proc.join()
    
    print(process)


def create_pool(n, data, function):
    pool = multiprocessing.Pool(processes=n)
    pool.map(function,data)
    pool.close()


def send(agent, data):
    agent.send(data)
    agent.close


def receive(agent):
    print(agent.recv())


if __name__=='__main__':
    process = []
    items = ['SpaceR', 'LunaLab', 'Rover', 'PhD']
    data = [5,10,15,25,7,12,24,38,55,90,14,74]

    #queue = multiprocessing.Queue()


    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)

    #manager = multiprocessing.Manager()
    #test_d = manager.dict()
    #test_d["ctr"] = 0
    #test_d["QUIT"] = False


    connection1, connection2 = multiprocessing.Pipe(True)
    
    com1 = connection.Connection('Test connection')
    com1.createPipe()

    agents=[]
    agent1 = agent.Agent(["data1-agent1","data2-agent1"], com1.entrance1, "agent1")
    agent2 = agent.Agent(["data1-agent2","data2-agent2"], com1.entrance2, "agent2")
    agents.append(agent1)
    agents.append(agent2)

    #for agent in agents:
    #    boot = multiprocessing.Process(target=agent1.startAgent())
    #    boot.start()
    #print('here')
    agent1.startAgent()
    agent2.startAgent()

    #test_d["QUIT"] = True
    agent1.agent.join()
    agent2.agent.join()
    time.sleep(10)
    #agent1.closeAgent()
    #agent2.closeAgent()

    #proc1 = multiprocessing.Process(target=send, args=(agent1, items))
    #proc2 = multiprocessing.Process(target=receive, args=(agent2, ))

    #proc1.start()
    #proc2.start()

    #proc1.join()
    #proc2.join()


    #create_process(100000, items)
    #create_pool(1, (data, queue), send)
    #create_pool(1, queue, receive)

    


    