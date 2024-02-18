from simpy import Environment, Resource
from Entities.container import Container
from typing import Any


class QuayCrane:
    """
    A resource class to represent the quay crane in the terminal.
    It contains the information about the quay crane and the useful methods to operate the quay crane.
    """

    def __init__(self, env: Environment, crane_id: int):
        """
        A constructor to set the simpy environment and crane id of the the crane
        It also make sure initially the crane is not holding any container, is free to use.
        @env: Simpy environment
        @crane_id: id to be assigned to the crane
        """
        self.env: Environment = env
        self.crane_id: int = crane_id
        self.resource: Resource = Resource(env, capacity=1)
        # sets the container holded by the crane to none.
        self.holding_container: Container = None
        self.busy: bool = False  # makes the crane available to be used.
        # time which the crane picked up a container from the vessel.
        self.pick_up_time: float = 0
        self.req = None

    def get_name(self) -> str:
        """
        @@returns- the name of the crane i.e. crane_<berth_id>
        """
        return f'crane_{self.crane_id}'

    def unload_container(self, container: Container) -> Any:
        """
        Makes the crane pick up a container from the vessel and caches the time at which the container was picked.
        @container - The container picked up by the crane.
        """
        self.pick_up_time = self.env.now
        print(
            f"Time: {self.pick_up_time} min, {self.get_name()} picked up {container.get_name()}.")
        # set the holding container to the container picked.
        self.holding_container = container

    def ready_to_unload_container(self, container: Container) -> Any:
        """
        Makes the crane ready to load the container inside a truck.
        @container - container picked up by the crane.
        """
        print(
            f"Time: {self.env.now} min, {self.get_name()} is ready to unload {container.get_name()}.")

    def load_container_to_truck(self):
        """
        Loads the container in a truck and checks if it's the last container
        If the container is last then, makes the crane ready to be assigned to another vessel.
        """
        if (self.holding_container.is_last_container):
            self.release()
        self.holding_container = None

    def acquire(self) -> Any:
        """
        Make the crane busy with a task.
        @@returns - the resource request.
        """
        self.busy = True
        return self.resource.request()

    def can_drop_container(self, container_unload_time: float) -> bool:
        """
        Checks if the crane can drop a container inside a truck or not.
        Checks if enough time has passed since the crane has picked up the container.
        @@return - if the crane is ready then True else False.
        """
        time_since_pick_up: float = self.env.now - self.pick_up_time
        can_drop: bool = time_since_pick_up >= container_unload_time
        return can_drop

    def release(self):
        """
        Releases the crane and make it available for the next task.
        """
        self.resource.release(self.req)
        self.busy = False

    def request(self) -> Any:
        """
        Request from the crane resource.
        @@returns - the new request made.
        """
        self.req = self.resource.request()
        return self.req
