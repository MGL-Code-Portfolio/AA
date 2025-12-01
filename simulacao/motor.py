import time
from simulacao.visualizador import Visualizador 

class MotorDeSimulacao:
    def __init__(self, ambiente, visualizador=None):
        self.ambiente = ambiente
        self.visualizador = visualizador if visualizador else Visualizador()

    def executa_episodio(self, max_passos, visual=False, delay=0.1):
        # --- 1. RESET DO ESTADO ---
        self.ambiente.passo_atual = 0
        self.ambiente.objetivo_alcancado = False
        
        # Reset para Recoleção (Recursos)
        if hasattr(self.ambiente, 'pontuacao_total'):
            self.ambiente.pontuacao_total = 0
            
            # CORREÇÃO AQUI: É OBRIGATÓRIO REGENERAR RECURSOS
            # Se não fizermos isto, a lista fica vazia porque o agente comeu tudo no episódio anterior
            if hasattr(self.ambiente, 'recursos') and hasattr(self.ambiente, '_gerar_recursos'):
                self.ambiente.recursos.clear() # Limpa o que sobrou
                self.ambiente._gerar_recursos() # Cria novos recursos

        # Reset para Labirinto (Opcional: Novo labirinto a cada episódio)
        # Se quiseres que o labirinto mude sempre, descomenta isto:
        # if hasattr(self.ambiente, 'gerar_obstaculos_validos'):
        #     self.ambiente.gerar_obstaculos_validos()

        # Reset dos Agentes
        for agente in self.ambiente.agentes:
            agente.posicao = (0, 0)
            agente.recompensa_acumulada = 0
            
            # O agente não pode começar o jogo já a carregar coisas
            if hasattr(agente, 'tem_recurso'):
                agente.tem_recurso = False

        # --- 2. CICLO PRINCIPAL ---
        while self.ambiente.passo_atual < max_passos:
            self.ambiente.passo_atual += 1
            
            # Atualizar (Dinâmica)
            self.ambiente.atualizacao()

            # Perceção e Decisão
            accoes = {}
            for agente in self.ambiente.agentes:
                accoes[agente] = agente.age(self.ambiente)

            # Execução
            terminou_simulacao = False
            for agente, accao in accoes.items():
                recompensa, fim = self.ambiente.agir(accao, agente)
                agente.avaliacaoEstadoAtual(recompensa, self.ambiente)
                
                if fim:
                    terminou_simulacao = True

            # Visualização
            if visual:
                self.visualizador.renderizar(self.ambiente)
                time.sleep(delay)

            if terminou_simulacao:
                break