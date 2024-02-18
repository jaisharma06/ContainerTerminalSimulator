from simpy import Environment, Resource
from typing import Any
from Entities.container import Container


class Truck:
    def __init__(self, truck_id: int,  env: Environment):
        self.truck_id: int = truck_id
        self.env: Environment = env
        self.busy: bool = False
        self.container: Container = None
        self.resource: Resource = Resource(env, capacity=1)
        self.pick_up_time = 0
        self.req = None

    def __str__(self) -> str:
        return f'truck_{self.truck_id}'

    def get_name(self) -> str:
        return f'truck_{self.truck_id}'

    def transport_container(self, crane_name: str, container: Container) -> None:
        print(f"Time: {self.env.now} min, {crane_name} has unloaded {container.get_name()} to the {self.get_name()} and {self.get_name()} is transporting it to the yard block.")
        if (container.is_last_container):
            print(f'Time: {self.env.now} min, {crane_name} is free now.')
        self.busy = True
        self.container = container
        self.pick_up_time = self.env.now

    def transported_container_back_to_terminal(self) -> None:
        print(f"Time: {self.env.now} min, {self.get_name()} has transported {self.container.get_name()} to the yard block and back to the terminal")
        self.busy = False
        self.container = None
        self.resource.release(self.req)

    def can_unload_container(self, container_unload_time: float = 6) -> bool:
        time_since_pickup = self.env.now - self.pick_up_time
        can_unload = time_since_pickup >= container_unload_time
        return can_unload

    def request(self) -> Any:
        self.req = self.resource.request()
        return self.req
