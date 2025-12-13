import random
from core.politica import Politica

class PoliticaQlearning(Politica):
    def __init__(self, accoes_possiveis, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.acoes = accoes_possiveis
        self.q_tabela = {} 
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.modo_treino = True

    def _get_q(self, estado, acao):
        h = hash(estado)
        if h not in self.q_tabela:
            self.q_tabela[h] = {a: 0.0 for a in self.acoes}
        return self.q_tabela[h][acao]

    def decidir(self, observacao, agente):
        if self.modo_treino and random.random() < self.epsilon:
            return random.choice(self.acoes)
        
        h = hash(observacao)
        if h not in self.q_tabela:
            return random.choice(self.acoes)
        
        return max(self.q_tabela[h], key=self.q_tabela[h].get)

    def atualizar(self, obs_antiga, accao, recompensa, obs_nova):
        if not self.modo_treino or obs_antiga is None:
            return

        q_atual = self._get_q(obs_antiga, accao)
        
        h_futuro = hash(obs_nova)
        if h_futuro not in self.q_tabela:
            self.q_tabela[h_futuro] = {a: 0.0 for a in self.acoes}
        
        max_q_futuro = max(self.q_tabela[h_futuro].values())
        
        # equação de bellman
        novo_q = q_atual + self.alpha * (recompensa + self.gamma * max_q_futuro - q_atual)
        self.q_tabela[hash(obs_antiga)][accao] = novo_q