import time
from simulacao.visualizador import Visualizador 

class MotorDeSimulacao:
    def __init__(self, ambiente, visualizador=None):
        self.ambiente = ambiente
        self.visualizador = visualizador if visualizador else Visualizador()

    def executa_episodio(self, max_passos, visual=False, delay=0.1):
        # RESET
        self.ambiente.passo_atual = 0
        self.ambiente.objetivo_alcancado = False
        
        if hasattr(self.ambiente, 'pontuacao_total'):
            self.ambiente.pontuacao_total = 0
            if hasattr(self.ambiente, 'recursos') and hasattr(self.ambiente, '_gerar_recursos'):
                self.ambiente.recursos.clear()
                self.ambiente._gerar_recursos()

        for agente in self.ambiente.agentes:
            agente.reset_stats() 
            # Regista a posição inicial como visitada
            agente.stats["celulas_visitadas"].add(agente.posicao)

        
        while self.ambiente.passo_atual < max_passos:
            self.ambiente.passo_atual += 1
            self.ambiente.atualizacao()

            accoes = {}
            for agente in self.ambiente.agentes:
                accoes[agente] = agente.age(self.ambiente)

            terminou_simulacao = False
            for agente, accao in accoes.items():
                recompensa, fim = self.ambiente.agir(accao, agente)
                agente.avaliacaoEstadoAtual(recompensa, self.ambiente)
                
                agente.stats["passos_episodio"] += 1
                agente.stats["celulas_visitadas"].add(agente.posicao)
                
                
                if recompensa == -0.5:
                    agente.stats["colisoes"] += 1
                

                if fim: terminou_simulacao = True

            if visual:
                self.visualizador.renderizar(self.ambiente)
                time.sleep(delay)

            if terminou_simulacao:
                break