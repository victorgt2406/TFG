from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar
from bridges.connector import Connector

L = TypeVar('L') # List type
P = TypeVar('P') # Place to store it or upload it

class Saver(Connector, ABC, Generic[L, P]):
    "Connector that save data"
    @abstractmethod
    async def save_data(self, data:List[L], place:P, **args) -> None:
        """Gets some data from a source and return it"""