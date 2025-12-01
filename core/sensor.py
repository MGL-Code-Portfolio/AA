from abc import ABC, abstractmethod
from typing import Dict

class Sensor(ABC):
    @abstractmethod
    def detetar(self, ambiente, agente) -> Dict:
        """Deve retornar um dicionário com dados percebidos."""
        pass