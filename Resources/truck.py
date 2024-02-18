# import the required modules and python files.
from simpy import Environment, Resource
from typing import Any
from Entities.container import Container


class Truck:
    """
    A resource class to represent trucks in a terminal.
    Contains important methods and information to control a truck on the terminal.
    """

    def __init__(self, truck_id: int,  env: Environment):
        """
        Constructor method to set the truck id, simpy env
        Set the default values of the truck i.e. container holding to none, busy: false etc.
        """
        self.truck_id: int = truck_id
        self.env: Environment = env
        self.busy: bool = False
        self.container: Container = None
        self.resource: Resource = Resource(env, capacity=1)
        self.pick_up_time = 0  # time at which the truck was loaded by a train.
        self.req = None

    def __str__(self) -> str:
        """
        overloaded method for object to string cast
        @@returns- the name of the truck in the format 'truck_<truck_id>.
        """
        return f'truck_{self.truck_id}'

    def get_name(self) -> str:
        """
        @@returns- the name of the truck in the format 'truck_<truck_id>.
        """
        return f'truck_{self.truck_id}'

    def transport_container(self, crane_name: str, container: Container) -> None:
        """
        Loads the truck with a container and the trucks starts heading it to the yard block.
        @crane_name: crane which loaded the container
        @container: container loaded inside the truck.
        """
        print(f"Time: {self.env.now} min, {crane_name} has unloaded {container.get_name()} to the {self.get_name()} and {self.get_name()} is transporting it to the yard block.")
        if (container.is_last_container):
            # sets the crane free if this was the last container.
            print(f'Time: {self.env.now} min, {crane_name} is free now.')
        self.busy = True  # sets the truck busy with a task.
        self.container = container  # sets the container loaded in the truck.
        self.pick_up_time = self.env.now  # caches the container load time.

    def drop_container_to_the_block(self) -> None:
        """
        Drops the container in the yard block and starts heading back to the terminal.
        """
        print(f'Time: {self.env.now} min, {self.get_name()} has dropped the {self.container.get_name()} at the yard block and is heading back to the terminal.')
        self.container = None  # resets the container to none.

    def head_back_to_terminal(self) -> None:
        """
        Resets the truck to free and releases all the resources when the trucks reaches the terminal back.
        """
        print(
            f"Time: {self.env.now} min, {self.get_name()} has reached back to the terminal.")
        self.busy = False  # sets not busy and can be used again.
        self.container = None
        self.resource.release(self.req)  # releases the resource in use.

    def can_unload_container(self, container_unload_time: float = 6) -> bool:
        """
        Checks if the truck can drop the container at the yard.
        It checks the total travel time and compares it with the general time taken to reach the yard.
        @@returns: True if truck can unload container else False.
        """
        time_since_pickup = self.env.now - self.pick_up_time
        can_unload = time_since_pickup >= container_unload_time / 2.0
        return can_unload

    def is_back_at_the_termial(self, container_unload_time=6) -> bool:
        """
        Checks if the truck is back at the terminal.
        It checks the total travel time and compares it with the general time taken to reach from the yard to the terminal.
        @@returns: True if truck has reached container else False.
        """
        time_since_pickup = self.env.now - self.pick_up_time
        can_unload = time_since_pickup >= container_unload_time
        return can_unload

    def request(self) -> Any:
        """
        Makes a new request to use the truck request.
        @@returns- new request made.
        """
        self.req = self.resource.request()
        return self.req
