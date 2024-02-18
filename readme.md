# Container Terminal Simulator

## Introduction

1. Simulate vessels arriving to the container terminal. The time between vessel arrivals follows an
exponential distribution with an average of 5 hours
(https://docs.python.org/3/library/random.html#random.expovariate). This is the input that drives the
simulation.
   - Each vessel carries 150 containers that needs to be discharged (unloaded).
2. The vessels will need to berth at the terminal and there are only 2 available slots (berth_1 & berth_2).
This means that if a vessel arrives and both berths are already occupied, the new vessel has to wait in
a queue (FIFO).
   - When all containers have been discharged, the vessel leaves and the berth slot is free to be
used by the next vessel.
3. Once the vessel berths, a quay crane [https://en.wikipedia.org/wiki/Container_crane](https://en.wikipedia.org/wiki/Container_crane) will start lifting
the containers from the vessel to a truck.
   - There are 2 quay cranes and any quay crane can operate on any berth
   - Both quay cranes cannot serve the same vessel
   - It takes the crane 3 minutes to move one container.
   - The crane must put the container on a truck. If no truck is available, the crane will have to wait
    until a truck is free before it can start its next move.
   - The crane can use any of the free trucks, it does not have to wait for the same truck to come
    back again. This means that if only one vessel is in berth, it will never be blocked by waiting for
    a truck. If two vessels are in beth, the cranes will sometimes be blocked while waiting for a free
    truck.
4. The terminal has 3 trucks, transporting containers from the quay cranes to the yard blocks
[https://en.wikipedia.org/wiki/Terminal_tractor](https://en.wikipedia.org/wiki/Terminal_tractor).
   - It takes the truck 6 minutes to drop off the container at the yard block and come back again
1. Create a simple log (print statements does the job) for each event, e.g. vessel arriving, vessel
berthing, quay crane moves a container, etc. The log should include the current time using SimPy Environment.now
[https://simpy.readthedocs.io/en/latest/api_reference/simpy.core.html#simpy.core.Environment.now](https://simpy.readthedocs.io/en/latest/api_reference/simpy.core.html#simpy.core.Environment.now).
6. Run the simulation for some time using env.run(until=SIMULATION_TIME) where SIMULATION_TIME
is a parameter the user can set.
7. The simulation time in SimPy is unitless but in this exercise we can assume 1 tick = 1 minute
----

</br>

## How to run
>- Open the root folder in a code editor.
>- Open the file '*Simulation/container_terminal_simulator.py*'
>- replace the path in the 'sys.path.append('**G:\Projects\Python\ContainerTerminalSimulator**')' with the absolute path of the root directory.
>- Run the file '*Simulation/container_terminal_simulator.py*'

