# ROSBlockchain
The readme part should be remake
## Introduction
The purpose of this project is to get familiar with multi-robot approaches for autonomous communication and data exchange. As a result, exchanges between robots don’t have to be relevant so raw data (like position, velocity or even a message) can successfully complete the objective.


At first, studying state of the art approaches, based on DLT and common blockchain technologies, is enough to start working on a first simulated approach (within a computer). Then communication between several computers can be achieved (teammates computers for example).


Last but not least,  a proof of concept can be achieved with an app/software installed in different rovers to test the communication system in real inlunar environments at the LunaLab facility.


A bonus could be to make a nice interface reachable on a laptop where all the communication between the rovers can be monitored. 


DLT : Decentralized Ledger Technologies


## Objectives:

1. Simulate communication inside one computer
    * Multithreading (without core consideration)
    * Multiprocess (one process for one core)

2. Simulate communication between multiple computers
    * Unstructured architecture (Unstructured peer to peer)
    * Structured architecture (Ring, random islands)

3. Connect two rovers in pairs (Share information between them)
ROS or ROS2

4. Communication between differents rovers
