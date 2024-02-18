# import for sys to set the root directory of the project to access the absolute path of the subdirectories.
import sys
# replace the 'G:\Projects\Python\ContainerTerminalSimulator' path with the absolute path of the root directory in the machine to set the root directory of the project.
sys.path.append('G:\Projects\Python\ContainerTerminalSimulator')

# import of required python classes which are accessed.
from simpy import Environment
from Entities.container_terminal import ContainerTerminal
from Configurations.config import Config



# Define and initialize the simpy environment.
env: Environment = Environment()
# setup terminal according to the configuration.
terminal: ContainerTerminal = ContainerTerminal(
    env, Config.BERTH_COUNT, Config.CRANE_COUNT, Config.TRUCK_COUNT)


def process_vessel_queue(env: Environment, terminal: ContainerTerminal):
    """
    process to simulate the container terminal
    - update_vessel_queue: checks if a new vessel has arrived 
        and if a new vessel has arrived then it adds it to a queue and assigns a berth and crane if berth and cranes are free on FIFO basis
    - process_berth: checks if the vessel has any containers left, if there are no containers left then, updates the vessel status to depart else if there are
        container then checks if the train assigned is free to pickup a container. in case, if train is free then the train picks up the container.
    - drop_containers_to_trucks: Checks if a train is holding any container and is ready to drop that container in a truck, then checks if the truck is free to 
        transport the container. If, a truck is free then the container is loaded inside the truck.
    - unload_containers_to_block: After loading the container, the truck departs to drop the container at block and come back to the terminal afterwards.

    @env: Simpy environment for the simulation
    @terminal: virtual terminal which manages the resources.
    """
    yield env.timeout(0)
    env.process(terminal.update_vessel_queue())
    env.process(terminal.process_berth())
    env.process(terminal.drop_containers_to_truck())
    env.process(terminal.unload_containers_to_block())


#Initializes the process of simulating a container terminal
env.process(process_vessel_queue(env, terminal))
#starts the actual process till provided time.
env.run(until=Config.SIMULATION_TIME)
