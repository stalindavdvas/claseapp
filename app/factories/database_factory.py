from abc import ABC, abstractmethod

class DatabaseFactory(ABC):
    @abstractmethod
    def create_connection(self):
        pass

    @abstractmethod
    def create_model(self):
        pass