from abc import ABC, abstractmethod

class Politica(ABC):
    @abstractmethod
    def decidir(self, observacao, agente): #retorna ação baseada na observação
        pass

    @abstractmethod
    def atualizar(self, obs_antiga, accao, recompensa, obs_nova): #atualiza o conhecimento com base na politica
        pass