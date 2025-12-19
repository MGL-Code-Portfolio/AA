from abc import ABC, abstractmethod
from typing import Dict

class Sensor(ABC):
    @abstractmethod
    def detetar(self, ambiente, agente) -> Dict: #retorna um dicionario com os dados observados
        pass