from simpy import Environment, Resource
from typing import Any

class BaseResource : 
    def __init__(self, env: Environment, resource_id : int):
        self.resource = Resource(env, capacity=1)
        self.req = None
        self.resource_id = resource_id

    def release(self)->None:
        self.resource.release(self.req)
    
    def request(self)-> Any:
        self.req = self.resource.request()
        return self.req
    
    def __str__(self) -> str:
        return self.get_name()
    
    def get_name(self) -> str:
        class_name = self._to_snake_case((self.__class__.__name__).lower())
        return f"{class_name}_{self.resource_id}"
    
    def _to_snake_case(self, word)-> str:
        snake_case : str = word[0].lower()
        for alphabet in word[1:]:
            if (alphabet.isupper()):
                snake_case += f'_{alphabet.lower()}'
            else:
                snake_case += alphabet
        return snake_case
