from core.politica import Politica
import random

class PoliticaAleatoria(Politica): # política que escolhe ações aleatoriamente, para comparação de desempenho das outras políticas
   
    def __init__(self, accoes_possiveis):
        self.accoes = accoes_possiveis

    def decidir(self, observacao, agente):
        return random.choice(self.accoes)

    def atualizar(self, obs_antiga, accao, recompensa, obs_nova):
        pass