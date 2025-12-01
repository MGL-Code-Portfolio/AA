import time
# Nota: Importamos o GUI aqui, mas vamos usar injeção de dependência no main
from simulacao.visualizador import Visualizador 

class MotorDeSimulacao:
    def __init__(self, ambiente, visualizador=None):
        self.ambiente = ambiente
        # Se não passarmos um visualizador, usa o básico (TUI)
        self.visualizador = visualizador if visualizador else Visualizador()

    def executa_episodio(self, max_passos, visual=False, delay=0.1):
        self.ambiente.passo_atual = 0
        self.ambiente.objetivo_alcancado = False
        
        # Reset Agentes
        for agente in self.ambiente.agentes:
            agente.posicao = (0, 0)
            agente.recompensa_acumulada = 0

        while self.ambiente.passo_atual < max_passos:
            self.ambiente.passo_atual += 1
            
            # 1. Atualizar Ambiente
            self.ambiente.atualizacao()

            # 2. Perceção e Decisão
            accoes = {}
            for agente in self.ambiente.agentes:
                accoes[agente] = agente.age(self.ambiente)

            # 3. Execução
            terminou = False
            for agente, accao in accoes.items():
                recompensa, fim = self.ambiente.agir(accao, agente)
                agente.avaliacaoEstadoAtual(recompensa, self.ambiente)
                if fim: terminou = True

            # 4. Visualização
            if visual:
                self.visualizador.renderizar(self.ambiente)
                time.sleep(delay)

            if terminou:
                break