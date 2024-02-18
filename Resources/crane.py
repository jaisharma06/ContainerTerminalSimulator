from simpy import Environment, Resource
from Entities.container import Container
from typing import Any


class QuayCrane:

    def __init__(self, env: Environment, crane_id: int):
        self.env: Environment = env
        self.crane_id: int = crane_id
        self.resource: Resource = Resource(env, capacity=1)
        self.holding_container: Container = None
        self.busy: bool = False
        self.pick_up_time: float = 0
        self.req = None

    def get_name(self) -> str:
        return f'crane_{self.crane_id}'

    def unload_container(self, container: Container) -> Any:
        self.pick_up_time = self.env.now
        print(
            f"Time: {self.pick_up_time} min, {self.get_name()} picked up {container.get_name()}.")
        self.holding_container = container

    def ready_to_unload_container(self, container: Container) -> Any:
        print(
            f"Time: {self.env.now} min, {self.get_name()} is ready to unload {container.get_name()}.")

    def load_container_to_truck(self):
        if (self.holding_container.is_last_container):
            self.release()
        self.holding_container = None

    def acquire(self) -> Any:
        self.busy = True
        return self.resource.request()

    def can_drop_container(self, container_unload_time: float) -> bool:
        time_since_pick_up: float = self.env.now - self.pick_up_time
        can_drop: bool = time_since_pick_up >= container_unload_time
        return can_drop

    def release(self):
        self.resource.release(self.req)
        self.busy = False

    def request(self) -> Any:
        self.req = self.resource.request()
        return self.req
