from abc import ABC, abstractmethod

class Connector(ABC):
    "Connector"
    def __init__(self, name="unnamed connector") -> None:
        self.name = name
        self.set_up()
        if name == "unnamed connector":
            print("WARNING: Unnamed connector")
        else:
            print(f"Connector: {name} RUNNING...")

    @abstractmethod
    def set_up(self):
        """Prepares the Fetcher or Saver to fetch_data"""