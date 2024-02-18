# Import required python files and modules
from Resources.berth import Berth
from Resources.crane import QuayCrane
from Resources.truck import Truck
from Entities.vessel import Vessel
from simpy import Environment
from typing import List
from random import expovariate
from Configurations.config import Config
from Entities.container import Container


class ContainerTerminal:
    """
    A virtual terminal class that replicates a real terminal for performing simulation.
    It handles all the resources and entitites i.e. Berth, QuayCrane, Truck, Vessel, Container.
    """

    def __init__(self, env: Environment, berth_count: int = 2, crane_count: int = 2, truck_count: int = 3):
        """
        Contructor method to initialize the terminal.
        - Sets the simulation environment for the terminal.
        - Initializes all the resources i.e. quay cranes, berths, trucks.
        - Initializes a queue for vessels which will be updated as soon as a vessel arrives in the terminal or when a vessel goes to the berth.

        @env: Simpy environment
        @berth_count: total available berths in the terminal.
        @crane_count: Number of quay cranes at the terminal.
        @truck_count: Number of trucks at the terminal
        """
        self.env: Environment = env
        self.berths: List[Berth] = [Berth(i, env)
                                    for i in range(1, berth_count + 1)]  # Creates berths with incremental ids starting from 1
        self.cranes: List[QuayCrane] = [
            QuayCrane(env, i) for i in range(1, crane_count + 1)]  # Creates quay cranes with incremental ids starting from 1
        self.trucks: List[Truck] = [Truck(i, env)
                                    for i in range(1, truck_count + 1)]  # Creates trucks with incremental ids starting from 1
        # Initializes an empty queue of vessels.
        self.vessels: List[Vessel] = []

    def process_berth(self):
        """
        -   checks if there are any vessels on any of the berths
        -   if there is a vessel on a berth then checks if the crane assigned to the vessel is free or not.
        -   if the crane is free then makes the crane pickup a container.
        -   if there are no containers in the vessel then makes the vessel depart from the berth and makes the berth ready to entertain another vessel.
        """
        while True:
            acquired_berths: List[Berth] = list(
                filter(lambda berth: berth.acquired is True, self.berths))  # Filters out all the berths which has a vessel assigned.
            if (len(acquired_berths) > 0):  # checks if there are any berths with a vessel assigned
                for berth in acquired_berths:
                    with berth.request() as req_berth:  # requests for a berth resource.
                        yield req_berth
                        vessel: Vessel = berth.vessel
                        crane: QuayCrane = vessel.crane
                        # checks if a crane is assigned to the vessel.
                        if (crane is not None):
                            # checks if there is any container remaining in the vessel.
                            if (vessel.get_remaining_container_count() > 0):
                                # checks if crane is holding any container.
                                if (crane.holding_container is None):
                                    # removes the container from the vessel.
                                    container: Container = vessel.unload_container()
                                    # asks the crane to pick up the container.
                                    crane.unload_container(container)
                            else:  # if no containers are available in the vessel.
                                # removes the crane assignment.
                                vessel.release_crane()
                                # makes the vessel depart from the terminal.
                                berth.release_vessel()
            yield self.env.timeout(Config.DELAY_FOR_CONTEXT_SWITCHING)

    def vessel_arrival(self, vessel_id: int, container_count: int = 150) -> Vessel:
        """
        Creates a new vessel with the provided id and container count.
        @vessel_id: unique id of the vessel.
        @container_count: Count of the containers inside the vessel.
        @@returns - Instantiated vessel.
        """
        vessel_id: int = vessel_id
        vessel: Vessel = Vessel(vessel_id,  self.env, container_count)
        self.vessels.append(vessel)
        print(f'Time: {self.env.now} min, {vessel.get_name()} arrived.')
        return vessel

    def update_vessel_queue(self):
        """
        Updates the vessel queue when a new vessel arrives at the terminal. The arrival time is random with exponential distribution.
        Creates a new vessel with incremental ids starting from 1.
        Steps
        - Creates a new vessel and adds it to the vessel queue.
        - Checks if a berth is available for the vessel, if any berth is available then on the FIFO basis allocates the berth to the first arrived vessel.
        - If there is a crane available then assigns that crane to the vessel which was sent to the berth.
        - increments the vessel id by 1 for the next vessel that will arrive.
        - Waits for next vessel to arrive.
        """
        vessel_id = 1
        while True:
            self.vessel_arrival(
                vessel_id, Config.CONTAINERS_PER_VESSEL)  # Creates a new vessel and adds it to the vessel queue.
            for berth in self.berths:
                with berth.request() as req:
                    yield req
                    if (not berth.acquired):  # for every berth checks if the berth is available
                        # removes the first vessel from the queue.
                        vessel: Vessel = self.vessels.pop(0)
                        # assigns the vessel to the berth.
                        berth.assign_vessel(vessel)
                        for crane in self.cranes:  # checks if any crane is free.
                            with crane.resource.request() as req:
                                yield req
                                if (not crane.busy):
                                    # assigns the free crane to the vessel.
                                    vessel.assign_crane(crane)
                                    break
                        break
            # increments the vessel id by 1 for the next vessel.
            vessel_id += 1
            # waits for an exponential time for the next vessel.
            yield self.env.timeout(expovariate(1/Config.TIME_BETWEEN_VESSELS))

    def drop_containers_to_truck(self):
        """
        Steps
        - Checks if any crane is holding any container and is ready to drop the container in a truck.
        - If there is any crane which is ready to drop the container then it waits for the truck to be available.
        - If any truck is available then the crane loads the container inside the truck and is ready to pickup the next container.
        - Updates the crane status so that the crane can pickup another container from the berth it is assigned to.
        """
        while True:
            for crane in self.cranes:
                # checks if the crane is holding any container.
                if (crane.holding_container):
                    # Checks if the crane can drop the container.
                    if (crane.can_drop_container(Config.TIME_OF_CRANE_UNLOAD)):
                        for truck in self.trucks:  # Checks if any truck is available.
                            with truck.request() as req:
                                yield req
                                if (truck.busy is False):
                                    # loads the container inside the truck.
                                    container: Container = crane.holding_container
                                    crane.load_container_to_truck()
                                    truck.transport_container(
                                        crane.get_name(), container)
                                    # updates the status of the crane so that it is ready to pickup another container.
                                    crane.holding_container = None
                                    break
            yield self.env.timeout(Config.DELAY_FOR_CONTEXT_SWITCHING)

    def unload_containers_to_block(self):
        """
        Steps
        - Checks if a truck has reached the block and is ready to drop the container at the block.
        - if the truck is ready to drop the container at the block then asks the truck to drop the container at the block and then the truck comes back to the terminal.
        """
        while True:
            # checks for all the trucks if they are carrying any container.
            for truck in self.trucks:
                with truck.request() as req:
                    yield req
                    if (truck.busy is True):
                        # Checks if the container has dropped the container.
                        if (truck.container is not None):
                            if (truck.can_unload_container(Config.TRUCK_TRANSPORTATION_TIME)):
                                # drops the container at the yard if the truck has reached the yard.
                                truck.drop_container_to_the_block()
                        else:
                            if (truck.can_unload_container(Config.TRUCK_TRANSPORTATION_TIME)):
                                # after dropping the container heads back to the terminal.
                                truck.head_back_to_terminal()

            yield self.env.timeout(Config.DELAY_FOR_CONTEXT_SWITCHING)
