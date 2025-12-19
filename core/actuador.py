from abc import ABC, abstractmethod

class Actuador(ABC): 
    @abstractmethod
    def executar(self, accao, agente, ambiente):
        pass