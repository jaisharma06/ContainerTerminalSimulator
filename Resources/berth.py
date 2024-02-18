from typing import List, Any
from simpy import Environment, Resource
from Entities.container import Container
from Resources.vessel import Vessel

class Berth:
    def __init__(self, berth_id : int, env : Environment):
        self.available_containers : List[Container] = []
        self.berth_id : int = berth_id
        self.acquired : bool = False
        self.vessel : Vessel = None
        self.env : Environment = env
        self.resource : Resource = Resource(env, capacity=1)
        self.req = None

    def acquire(self) -> Any:
        self.acquired = True
        return self.resource.request()
    
    def release(self) -> None:
        self.acquired = False
        self.vessel = None
        self.resource.release(self.req)
    
    def add_available_container(self, container: Container) -> None:
        self.available_containers.append(container)
    
    def pick_up_container_from_berth(self) -> Container:
        return self.available_containers.pop()
    
    def get_name(self):
        return f'berth_{self.berth_id}'

    def assign_vessel(self, vessel : Vessel) -> None:
        self.vessel : Vessel = vessel
        print(f'Time: {self.env.now} min, {self.get_name()} assigned to {vessel.get_name()}.')
        self.acquired = True
    
    def release_vessel(self) -> None:
        print(f'Time: {self.env.now} min, {self.vessel.get_name()} departs now.')
        self.release()

    def request(self) -> Any:
        self.req = self.resource.request()
        return self.req