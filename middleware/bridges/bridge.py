"Bridges"

from abc import ABC, abstractmethod
import time
from typing import Generic, Type, TypeVar

from .fetcher import Fetcher
from .saver import Saver


# Define type variables for fetcher and saver
F = TypeVar('F', bound=Fetcher)
S = TypeVar('S', bound=Saver)


class Bridge(ABC, Generic[F, S]):
    """
    Abstract class of bridge
    """

    def __init__(self, name: str, fetcher_class: Type[F], saver_class: Type[S]) -> None:

        self.name = name
        # Fetcher
        self._fetcher_class: Type[F] = fetcher_class
        self.fetcher: F = self._fetcher_class()
        # Saver
        self._saver_class: Type[S] = saver_class
        self.saver: S = self._saver_class()

    def setup(self):
        "Update the credentials to Elasticsearch and Msgraph"
        self.saver = self._saver_class()
        self.fetcher = self._fetcher_class()

    @abstractmethod
    async def update_data(self):
        ...

    async def run_once(self):
        "Runs one update data"
        self.setup()
        start_time = time.time()
        await self.update_data()
        end_time = time.time()

        total_time = end_time - start_time
        print(f"INFO: Bridge {self.name}: took {total_time:.2f} secs")