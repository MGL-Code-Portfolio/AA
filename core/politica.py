from abc import ABC, abstractmethod

class Politica(ABC):
    @abstractmethod
    def decidir(self, observacao, agente):
        """Retorna uma ação baseada na observação."""
        pass

    @abstractmethod
    def atualizar(self, obs_antiga, accao, recompensa, obs_nova):
        """Atualiza o conhecimento interno (Learning Mode)."""
        pass