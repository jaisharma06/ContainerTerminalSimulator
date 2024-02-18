# import the required modules and python files.
from typing import Any
from simpy import Environment, Resource
from Entities.vessel import Vessel


class Berth:
    """
    A resource class for the berth entity that represent the real berth present at a terminal.
    It contains the information about the berth i.e. if the berth is currently in use, berth id, assigned vessel. 
    """

    def __init__(self, berth_id: int, env: Environment):
        """
        Contstructor for berth class.
        assigns a berth id and sets the simulation environment. Initially sets the berth ready to be used. 
        Makes sure no vessel is assigned to the berth initially

        @berth_id: Id to be assigned to the berth.
        @env: Simpy environment for simulation.
        """
        self.berth_id: int = berth_id
        self.acquired: bool = False
        self.vessel: Vessel = None
        self.env: Environment = env
        self.resource: Resource = Resource(env, capacity=1)
        self.req = None

    def acquire(self) -> Any:
        """
        Sets the berth in use and returns the resource request.
        @@return - Resource request for the berth.
        """
        self.acquired = True
        return self.resource.request()

    def release(self) -> None:
        """
        Releases the berth resource and sets the assigned vessel to None.
        """
        self.acquired = False
        self.vessel = None
        self.resource.release(self.req)

    def get_name(self):
        """
        @@returns- the name of the berth i.e. berth_<berth_id>
        """
        return f'berth_{self.berth_id}'

    def assign_vessel(self, vessel: Vessel) -> None:
        """
        Assigns a new vessel to the berth and logs the time at which berth was assigned.
        sets the berth busy.
        """
        self.vessel: Vessel = vessel
        print(
            f'Time: {self.env.now} min, {self.get_name()} assigned to {vessel.get_name()}.')
        self.acquired = True

    def release_vessel(self) -> None:
        """
        Makes the vessel depart and makes the berth avaiable to entertain new vessel.
        """
        print(
            f'Time: {self.env.now} min, {self.vessel.get_name()} departs now.')
        self.release()

    def request(self) -> Any:
        """
        Makes a new request for the berth resource
        @@returns- the new request generated.
        """
        self.req = self.resource.request()
        return self.req
