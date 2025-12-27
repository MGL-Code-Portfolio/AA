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
        agente.posicao_inicial = pos_inicial
        self.agentes.append(agente)

    @abstractmethod
    def agir(self, accao, agente) -> tuple[float, bool]:
        pass
    
    @abstractmethod
    def estado_global(self):
        pass
    
    @abstractmethod
    def atualizacao(self):
        pass