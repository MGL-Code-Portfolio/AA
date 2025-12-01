import pygame
import sys

class VisualizadorGUI:
    def __init__(self, largura_grelha, altura_grelha, tamanho_celula=60):
        self.largura = largura_grelha
        self.altura = altura_grelha
        self.tamanho_celula = tamanho_celula
        
        pygame.init()
        self.largura_ecra = self.largura * self.tamanho_celula
        self.altura_ecra = self.altura * self.tamanho_celula
        self.screen = pygame.display.set_mode((self.largura_ecra, self.altura_ecra))
        pygame.display.set_caption("Simulador SMA - Multi-Ambiente")
        
        self.font = pygame.font.Font(None, 24)

    def renderizar(self, ambiente):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        self.screen.fill((255, 255, 255)) # Fundo Branco

        # 1. Desenhar Grelha
        for x in range(0, self.largura_ecra, self.tamanho_celula):
            pygame.draw.line(self.screen, (220, 220, 220), (x, 0), (x, self.altura_ecra))
        for y in range(0, self.altura_ecra, self.tamanho_celula):
            pygame.draw.line(self.screen, (220, 220, 220), (0, y), (self.largura_ecra, y))

        # 2. Desenhar Obstáculos (Labirinto) - PRETO
        if hasattr(ambiente, 'obstaculos'):
            for (ox, oy) in ambiente.obstaculos:
                rect = (ox*self.tamanho_celula, oy*self.tamanho_celula, self.tamanho_celula, self.tamanho_celula)
                pygame.draw.rect(self.screen, (0, 0, 0), rect)

        # 3. Desenhar Ninho (Recoleção) - CASTANHO
        if hasattr(ambiente, 'ninho_pos'):
            nx, ny = ambiente.ninho_pos
            rect = (nx*self.tamanho_celula, ny*self.tamanho_celula, self.tamanho_celula, self.tamanho_celula)
            pygame.draw.rect(self.screen, (139, 69, 19), rect) # Castanho

        # 4. Desenhar Recursos (Recoleção) - VERDE
        if hasattr(ambiente, 'recursos'):
            for (rx, ry) in ambiente.recursos:
                centro = (rx*self.tamanho_celula + self.tamanho_celula//2, ry*self.tamanho_celula + self.tamanho_celula//2)
                pygame.draw.circle(self.screen, (0, 200, 0), centro, self.tamanho_celula//4)

        # 5. Desenhar Farol (Farol) - AMARELO
        if hasattr(ambiente, 'posicao_farol'):
            fx, fy = ambiente.posicao_farol
            centro = (fx*self.tamanho_celula + self.tamanho_celula//2, fy*self.tamanho_celula + self.tamanho_celula//2)
            pygame.draw.circle(self.screen, (255, 215, 0), centro, self.tamanho_celula//3)

        # 6. Desenhar Agentes - AZUL (ou VERMELHO se tiver recurso)
        for agente in ambiente.agentes:
            ax, ay = agente.posicao
            cor = (0, 0, 255) # Azul padrão
            
            # Se o agente tiver um recurso (propriedade dinâmica), muda de cor
            if getattr(agente, 'tem_recurso', False):
                cor = (255, 0, 0) # Vermelho se carregar algo

            rect = (ax*self.tamanho_celula + 10, ay*self.tamanho_celula + 10, self.tamanho_celula - 20, self.tamanho_celula - 20)
            pygame.draw.rect(self.screen, cor, rect, border_radius=5)

        pygame.display.flip()

    def fechar(self):
        pygame.quit()