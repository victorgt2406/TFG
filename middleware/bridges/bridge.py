"Bridges"

from abc import ABC, abstractmethod
import time

class Bridge(ABC):
    """
    Abstract class of bridge
    """

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def setup(self):
        ...

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