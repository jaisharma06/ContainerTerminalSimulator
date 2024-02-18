from Entities.container import Container
from simpy import Environment, Resource
from Resources.crane import QuayCrane
from typing import Any


class Vessel:
    def __init__(self, vessel_id: int, env: Environment,  container_count: int = 150):
        self.vessel_id = vessel_id
        self.containers = [Container(i, i is container_count)
                           for i in range(1, container_count + 1)]
        self.env = env
        self.crane: QuayCrane = None
        self.resource: Resource = Resource(env, capacity=1)
        self.req: Any = None

    def get_remaining_container_count(self) -> int:
        return len(self.containers)

    def unload_container(self) -> Container:
        if (self.get_remaining_container_count() < 1):
            return None
        else:
            container: Container = self.containers.pop(0)
            return container

    def depart_vessel(self) -> None:
        self.berth = None

    def __str__(self) -> str:
        return f'vessel_{self.vessel_id}'

    def get_name(self) -> str:
        return f'vessel_{self.vessel_id}'

    def assign_crane(self, crane: QuayCrane) -> None:
        self.crane = crane
        crane.busy = True
        print(
            f'Time: {self.env.now} min, {self.crane.get_name()} assigned to {self}.')

    def release_crane(self) -> None:
        self.crane = None

    def request(self):
        self.req = self.resource.request()
        return self.req
