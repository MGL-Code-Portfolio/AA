import random
import math
from dominio.politica_qlearning import PoliticaQlearning

class PoliticaNovelty(PoliticaQlearning):
    def __init__(self, accoes_possiveis, k_vizinhos=15, limite_arquivo=500, alpha=0.1, gamma=0.9, epsilon=0.1):
        super().__init__(accoes_possiveis, alpha, gamma, epsilon)
        self.k_vizinhos = k_vizinhos
        self.limite_arquivo = limite_arquivo
        self.arquivo_comportamentos = [] # Lista de pontos comportamentais (centroides)
        self.buffer_episodio = [] # Armazena transições do episódio atual: (obs, accao, obs_nova)

    def atualizar(self, obs_antiga, accao, recompensa, obs_nova):
        """
        Em vez de atualizar a Q-Table imediatamente com a recompensa externa,
        guardamos a transição para processar no final do episódio com a recompensa intrínseca.
        Acumulamos também a recompensa externa.
        """
        if self.modo_treino:
            self.buffer_episodio.append((obs_antiga, accao, recompensa, obs_nova))

    def _calcular_centroide(self, agente):
        """
        Calcula o comportamento do agente.
        Modificado para usar apenas a posição final do agente,
        que é mais robusto para tarefas de navegação com objetivos.
        """
        # Usa a posição final do agente
        return agente.posicao

    def _distancia_euclidiana(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def finalizar_episodio(self, agente):
        """
        Chamado pelo Motor no fim do episódio.
        Calcula a novidade e aplica o aprendizado.
        """
        if not self.modo_treino:
            self.buffer_episodio.clear()
            return

        # 1. Caracterizar o comportamento (Posição Final)
        comportamento_atual = self._calcular_centroide(agente)

        # 2. Calcular Novidade (Distância média para os k vizinhos mais próximos no arquivo)
        recompensa_intrinsica = 0.0

        if len(self.arquivo_comportamentos) > 0:
            distancias = [self._distancia_euclidiana(comportamento_atual, comp) for comp in self.arquivo_comportamentos]
            distancias.sort()

            k = min(len(distancias), self.k_vizinhos)
            vizinhos_proximos = distancias[:k]

            if k > 0:
                recompensa_intrinsica = sum(vizinhos_proximos) / k
            else:
                recompensa_intrinsica = 1.0 # Valor base se arquivo vazio (primeiro episódio)
        else:
            recompensa_intrinsica = 1.0 # Primeiro episódio é sempre novidade

        # 3. Atualizar Arquivo (Adiciona comportamento atual)
        self.arquivo_comportamentos.append(comportamento_atual)
        if len(self.arquivo_comportamentos) > self.limite_arquivo:
            # Remove o mais antigo ou aleatório? Vamos remover o mais antigo (FIFO) para adaptação contínua
            self.arquivo_comportamentos.pop(0)

        # 4. Calcular Recompensa Externa Acumulada
        recompensa_externa_total = sum(r for _, _, r, _ in self.buffer_episodio)

        # 5. Atualizar Q-Table
        # Replay do episódio. A recompensa combinada é atribuída apenas ao último passo.
        recompensa_final = recompensa_intrinsica + recompensa_externa_total

        # Iteramos de trás para frente para permitir que o valor propague
        for i, (obs, accao, r_ext, obs_nova) in enumerate(reversed(self.buffer_episodio)):
            r = 0.0
            # Na iteração reversa, o primeiro elemento (i=0) corresponde ao último passo do episódio
            if i == 0:
                r = recompensa_final

            super().atualizar(obs, accao, r, obs_nova)

        # Limpar buffer para o próximo episódio
        self.buffer_episodio.clear()

        # Opcional: Log para debug
        # print(f"Novidade: {recompensa_intrinsica:.4f} | Comportamento: {comportamento_atual}")
