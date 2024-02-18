import sys
sys.path.append('G:\Projects\Python\ContainerTerminalSimulator')

from random import expovariate
from simpy import Environment
from Entities.container_terminal import ContainerTerminal
from Resources.vessel import Vessel
from Resources.crane import QuayCrane
from Entities.container import Container
from typing import Any, List
from Resources.berth import Berth
from Configurations.config import Config


env: Environment = Environment()
terminal: ContainerTerminal = ContainerTerminal(
    env, Config.BERTH_COUNT, Config.CRANE_COUNT, Config.TRUCK_COUNT)


def update_vessel_queue(env: Environment, terminal: ContainerTerminal) -> Any:
    vessel_id = 1
    while True:
        terminal.vessel_arrival(
            vessel_id, env, Config.CONTAINERS_PER_VESSEL, Config.TIME_BETWEEN_VESSELS)
        for berth in terminal.berths:
            with berth.request() as req:
                yield req
                if (not berth.acquired):
                    vessel: Vessel = terminal.vessels.pop(0)
                    berth.assign_vessel(vessel)
                    if (vessel.crane is None):
                        for crane in terminal.cranes:
                            with crane.resource.request() as req:
                                yield req
                                if (not crane.busy):
                                    vessel.assign_crane(crane)
                                    break
                    break
        vessel_id += 1
        yield env.timeout(expovariate(1/Config.TIME_BETWEEN_VESSELS))


def process_vessel_queue(env: Environment, terminal: ContainerTerminal) -> Any:
    yield env.timeout(0)
    env.process(update_vessel_queue(env, terminal))
    env.process(process_berth(env, terminal, terminal.berths[0]))
    env.process(drop_containers_to_truck(env, terminal))
    env.process(unload_containers_to_block(env, terminal))


def process_berth(env: Environment, terminal: ContainerTerminal, berth: Berth) -> Any:
    while True:
        acquired_berths: List[Berth] = list(
            filter(lambda berth: berth.acquired is True, terminal.berths))
        if (len(acquired_berths) > 0):
            for berth in acquired_berths:
                with berth.request() as req_berth:
                    yield req_berth
                    process_berth(env, terminal, berth)
                    vessel: Vessel = berth.vessel
                    with vessel.request() as req_ves:
                        yield req_ves
                        crane: QuayCrane = vessel.crane
                        if (vessel.get_remaining_container_count() > 0):
                            if (crane.holding_container is None):
                                container: Container = vessel.unload_container()
                                crane.unload_container(container)
                        else:
                            vessel.release_crane()
                            berth.release_vessel()
        yield env.timeout(0.001)


def drop_containers_to_truck(env: Environment, terminal: ContainerTerminal) -> Any:
    while True:
        for crane in terminal.cranes:
            if (crane.holding_container):
                if (crane.can_drop_container(Config.TIME_OF_CRANE_UNLOAD)):
                    for truck in terminal.trucks:
                        with truck.request() as req:
                            yield req
                            if (truck.busy is False):
                                container: Container = crane.holding_container
                                crane.load_container_to_truck()
                                truck.transport_container(
                                    crane.get_name(), container)
                                crane.holding_container = None
                                break
        yield env.timeout(0.001)


def unload_containers_to_block(env: Environment, terminal: ContainerTerminal) -> Any:
    while True:
        for truck in terminal.trucks:
            with truck.request() as req:
                yield req
                if (truck.busy is True):
                    if (truck.can_unload_container(Config.TRUCK_TRANSPORTATION_TIME)):
                        truck.transported_container_back_to_terminal()

        yield env.timeout(0.01)


env.process(process_vessel_queue(env, terminal))
env.run(until=Config.SIMULATION_TIME)
