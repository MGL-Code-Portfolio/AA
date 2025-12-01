from abc import ABC, abstractmethod
from typing import List
from core.agente import Agente

class Ambiente(ABC):
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.agentes: List[Agente] = []
        self.passo_atual = 0

    def adicionar_agente(self, agente: Agente, pos_inicial=(0,0)):
        agente.posicao = pos_inicial
        self.agentes.append(agente)

    @abstractmethod
    def agir(self, accao, agente) -> tuple[float, bool]:
        """Retorna (recompensa, terminou)."""
        pass
    
    @abstractmethod
    def estado_global(self):
        """Retorna representação para visualização."""
        pass
    
    @abstractmethod
    def atualizacao(self):
        """Passo 4 do Diagrama: Dinâmica do ambiente"""
        pass