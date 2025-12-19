import random
import pickle
import os
from core.politica import Politica

class PoliticaQlearning(Politica):
    def __init__(self, accoes_possiveis, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.acoes = accoes_possiveis
        self.q_tabela = {} 
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.modo_treino = True

    def _get_state_key(self, obs):
        """Gera uma chave estável e serializável para o estado."""
        if obs is None:
            return None
        # Usa uma tupla ordenada dos itens do dicionário para garantir estabilidade e imutabilidade
        return tuple(sorted(obs.dados.items()))

    def _get_q(self, estado, acao):
        # h = hash(estado) -> Removido por ser instável
        key = self._get_state_key(estado)
        if key not in self.q_tabela:
            self.q_tabela[key] = {a: 0.0 for a in self.acoes}
        return self.q_tabela[key][acao]

    def decidir(self, observacao, agente):
        if self.modo_treino and random.random() < self.epsilon:
            return random.choice(self.acoes)
        
        # h = hash(observacao) -> Removido
        key = self._get_state_key(observacao)

        if key not in self.q_tabela:
            return random.choice(self.acoes)
        
        return max(self.q_tabela[key], key=self.q_tabela[key].get)

    def atualizar(self, obs_antiga, accao, recompensa, obs_nova):
        if not self.modo_treino or obs_antiga is None:
            return

        q_atual = self._get_q(obs_antiga, accao)
        
        # h_futuro = hash(obs_nova) -> Removido
        key_futuro = self._get_state_key(obs_nova)

        if key_futuro not in self.q_tabela:
            self.q_tabela[key_futuro] = {a: 0.0 for a in self.acoes}
        
        max_q_futuro = max(self.q_tabela[key_futuro].values())
        
        # equação de bellman
        novo_q = q_atual + self.alpha * (recompensa + self.gamma * max_q_futuro - q_atual)

        key_antiga = self._get_state_key(obs_antiga)
        self.q_tabela[key_antiga][accao] = novo_q

    def guardar_tabela(self, nome_ficheiro):
        """Guarda a tabela Q num ficheiro pickle."""
        try:
            with open(nome_ficheiro, 'wb') as f:
                pickle.dump(self.q_tabela, f)
            print(f"Tabela Q guardada com sucesso em '{nome_ficheiro}'.")
        except Exception as e:
            print(f"Erro ao guardar tabela Q: {e}")

    def carregar_tabela(self, nome_ficheiro):
        """Carrega a tabela Q de um ficheiro pickle."""
        if not os.path.exists(nome_ficheiro):
            print(f"Ficheiro '{nome_ficheiro}' não encontrado.")
            return False

        try:
            with open(nome_ficheiro, 'rb') as f:
                self.q_tabela = pickle.load(f)
            print(f"Tabela Q carregada de '{nome_ficheiro}'. ({len(self.q_tabela)} estados)")
            return True
        except Exception as e:
            print(f"Erro ao carregar tabela Q: {e}")
            return False
