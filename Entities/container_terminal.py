from Resources.berth import Berth
from Resources.crane import QuayCrane
from Resources.truck import Truck
from Resources.vessel import Vessel
from simpy import Environment
from typing import Any, List

class ContainerTerminal:
    def __init__(self, env: Environment, berth_count : int = 2, crane_count : int = 2, truck_count : int = 3):
        self.env : Environment = env
        self.berths : List[Berth] = [Berth(i, env) for i in range(1, berth_count + 1)]
        self.cranes : List[QuayCrane] = [QuayCrane(env, i) for i in range(1, crane_count + 1)]
        self.trucks : List[Truck] = [Truck(i, env) for i in range(1, truck_count + 1)]
        self.vessels : List[Vessel] = []
    
    def vessel_arrival(self, vessel_id: int,env : Environment, container_count : int = 150,  time_between_vessel : float = 1/5)->Vessel:
        vessel_id : int = vessel_id
        vessel : Vessel = Vessel(vessel_id, self.env, container_count)
        self.vessels.append(vessel)
        print(f'Time: {self.env.now} min, {vessel.get_name()} arrived.')
        return vessel

    def assign_crane_to_vessel(self, vessel : Vessel):
        for crane in self.cranes:
            with crane.resource.request() as req:
                yield req
                if not crane.busy:
                    vessel.assign_crane(crane)
                    break

    def assign_berth_to_first_vessel(self)-> Any:
        if(len(self.vessels) < 1):
            print(len(self.vessels))
            return
        vessel = self.vessels.pop(0)
        for berth in self.berths:
            with berth.resource.request() as req:
                yield req
                if not berth.acquired:
                      berth.assign_vessel(vessel)
                      self.env.process(self.assign_crane_to_vessel(vessel))
                      break;
        

        