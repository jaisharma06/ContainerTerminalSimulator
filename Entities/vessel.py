# import the required modules and python files.
from Entities.container import Container
from simpy import Environment
from Resources.crane import QuayCrane


class Vessel():
    """
    An entity class to represent real life vessels.
    Contains the details about the vessel i.e. vessel id, total containers inside the vessel and allows operations related to the vessel.
    """

    def __init__(self, vessel_id: int, env: Environment,  container_count: int = 150):
        """
        A constructor for the vessel
        It sets the vessel id
        Initializes the vessel with all the containers.
        Set the simpy environment for simulation.
        Makes sure no quay crane is assigned to the vessel initially.
        """
        self.vessel_id = vessel_id
        self.containers = [Container(i, i is container_count)
                           for i in range(1, container_count + 1)]
        self.env = env
        self.crane: QuayCrane = None

    def get_remaining_container_count(self) -> int:
        """
        @@returns - Remaining containers count inside the vessel.
        """
        return len(self.containers)

    def unload_container(self) -> Container:
        """
        Checks if there is any container inside the vessel
        If there is any container left then, returns the container in order FIFO.
        @@returns- the container which was loaded first inside the vessel.
        """
        if (self.get_remaining_container_count() < 1):
            return None
        else:
            container: Container = self.containers.pop(0)
            return container

    def depart_vessel(self) -> None:
        """
        Removes the berth assigned to the vessel.
        """
        self.berth = None

    def get_name(self) -> str:
        """
        @@returns- the name of the vessel in the format 'vessel_<vessel_id>.
        """
        return f'vessel_{self.vessel_id}'

    def assign_crane(self, crane: QuayCrane) -> None:
        """
        Assigns a new quay crane to the vessel.
        @crane - the new crane to be assigned to the vessel.
        """
        self.crane = crane
        crane.busy = True
        print(
            f'Time: {self.env.now} min, {self.crane.get_name()} assigned to {self.get_name()}.')

    def release_crane(self) -> None:
        """
        Releases the crane assigned to the vessel.
        """
        self.crane = None
