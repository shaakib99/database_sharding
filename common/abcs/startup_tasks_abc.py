from abc import ABC, abstractmethod

class StartupTasksABC(ABC):
    @staticmethod
    @abstractmethod
    async def load():
        pass