from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

L = TypeVar('L') # List type
P = TypeVar('P') # Place to store it or upload it


class Fetcher(Connector, ABC, Generic[L, P]):
    "Connector that can fetch data"
    @abstractmethod
    async def fetch_data(self, place:P, **args) -> List[L]:
        """Gets some data from a source and return it"""