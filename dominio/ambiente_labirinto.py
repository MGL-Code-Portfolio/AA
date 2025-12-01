from core.ambiente import Ambiente

class AmbienteLabirinto(Ambiente):
    def __init__(self, largura, altura):
        super().__init__(largura, altura)
        # Saída no canto inferior direito
        self.saida_pos = (largura - 1, altura - 1)
        # Definir Paredes (Obstáculos) fixos para teste
        self.obstaculos = {
            (1, 1), (1, 2), (1, 3), # Parede vertical
            (3, 1), (3, 3), (3, 4), 
            (4, 1)
        }
        self.objetivo_alcancado = False

    def atualizacao(self):
        pass # Labirinto estático

    def agir(self, accao, agente):
        x, y = agente.posicao
        dx, dy = 0, 0
        
        if accao == 'N': dy = -1
        elif accao == 'S': dy = 1
        elif accao == 'O': dx = -1
        elif accao == 'E': dx = 1
        
        nx, ny = x + dx, y + dy
        
        # Verificar Limites do Mundo
        if 0 <= nx < self.largura and 0 <= ny < self.altura:
            # Verificar Colisão com Obstáculos
            if (nx, ny) not in self.obstaculos:
                agente.posicao = (nx, ny)
            else:
                # Bateu na parede: penalização leve e não move
                return -0.5, False
        
        # Verificar Vitória
        if agente.posicao == self.saida_pos:
            self.objetivo_alcancado = True
            return 20.0, True # Recompensa maior por sair
            
        return -0.1, False # Custo por passo
    
    def estado_global(self):
        return "Labirinto Visual" # O VisualizadorGUI trata disto