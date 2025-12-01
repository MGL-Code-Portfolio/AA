import time
from simulacao.visualizador import Visualizador

class MotorDeSimulacao:
    def __init__(self, ambiente):
        self.ambiente = ambiente
        self.visualizador = Visualizador()

    def executa_episodio(self, max_passos, visual=False, delay=0.1):
        # Passo 1 e 2: Inicialização do Estado
        self.ambiente.passo_atual = 0
        self.ambiente.objetivo_alcancado = False
        
        # Reset Agentes (equivalente a recarregar estado inicial)
        for agente in self.ambiente.agentes:
            agente.posicao = (0, 0)
            agente.recompensa_acumulada = 0

        # Início do Ciclo de Tempo (Loop)
        while self.ambiente.passo_atual < max_passos:
            self.ambiente.passo_atual += 1
            
            # --- PASSO 4 DO DIAGRAMA: Atualizar o Ambiente ---
            # (Ex: Recursos crescem, obstáculos movem-se)
            self.ambiente.atualizacao()

            # --- PASSO 5 e 6 DO DIAGRAMA: Perceção e Deliberação ---
            # Bloco [par]: Todos os agentes pensam ao mesmo tempo (logicamente)
            accoes_pendentes = {}
            for agente in self.ambiente.agentes:
                # agente.age() chama internamente:
                # 5.1 Solicitar Estado Local (agente.observacao)
                # 5.2 Devolver Percepção
                # 6. Deliberar (agente.politica.decidir)
                accoes_pendentes[agente] = agente.age(self.ambiente)

            # --- PASSO 7 DO DIAGRAMA: Execução da Ação ---
            # Bloco [par]: Todas as ações são aplicadas
            terminou_simulacao = False
            
            for agente, accao in accoes_pendentes.items():
                # 7.1 Tentar Executar Ação
                # 7.3 Devolver Resultado (Recompensa)
                recompensa, terminou_agente = self.ambiente.agir(accao, agente)
                
                # O agente recebe o feedback imediatamente
                agente.avaliacaoEstadoAtual(recompensa, self.ambiente)
                
                if terminou_agente:
                    terminou_simulacao = True

            # --- PASSO 8 e 9: Registar Estado e Verificar Terminação ---
            if visual:
                self.visualizador.renderizar(self.ambiente)
                time.sleep(delay)

            if terminou_simulacao:
                # Passo 10: Terminar Simulação
                break