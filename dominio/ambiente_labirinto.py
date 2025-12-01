from core.ambiente import Ambiente
import random
from collections import deque # Usado para o algoritmo de busca (BFS)

class AmbienteLabirinto(Ambiente):
    def __init__(self, largura, altura, densidade_paredes=0.25):
        super().__init__(largura, altura)
        
        self.inicio_pos = (0, 0)
        self.saida_pos = (largura - 1, altura - 1)
        self.obstaculos = set()
        self.densidade = densidade_paredes
        self.objetivo_alcancado = False
        
        # Garante que o mapa gerado tem solução
        self.gerar_obstaculos_validos()

    def gerar_obstaculos_validos(self):
        """Tenta gerar mapas aleatórios até encontrar um que tenha solução."""
        max_tentativas = 100
        
        for _ in range(max_tentativas):
            self.obstaculos.clear()
            self._preencher_obstaculos_aleatorios()
            
            # Se existir um caminho do Início até à Saída, aceitamos este mapa
            if self.existe_caminho():
                return 
        
        # Se falhar muitas vezes (ex: densidade muito alta), limpa o mapa para não crashar
        print("Aviso: Não foi possível gerar labirinto complexo. A criar mapa vazio.")
        self.obstaculos.clear()

    def _preencher_obstaculos_aleatorios(self):
        """Espalha obstáculos, protegendo apenas o início e o fim."""
        for x in range(self.largura):
            for y in range(self.altura):
                # Nunca colocar parede no início ou no fim
                if (x, y) == self.inicio_pos or (x, y) == self.saida_pos:
                    continue
                
                if random.random() < self.densidade:
                    self.obstaculos.add((x, y))

    def existe_caminho(self):
        """Usa BFS (Busca em Largura) para ver se é possível chegar à saída."""
        fila = deque([self.inicio_pos])
        visitados = {self.inicio_pos}
        
        while fila:
            x, y = fila.popleft()
            
            if (x, y) == self.saida_pos:
                return True # Encontrou caminho!
            
            # Verificar vizinhos (Cima, Baixo, Esq, Dir)
            vizinhos = [
                (x, y-1), (x, y+1), (x-1, y), (x+1, y)
            ]
            
            for nx, ny in vizinhos:
                # Se está dentro do mapa...
                if 0 <= nx < self.largura and 0 <= ny < self.altura:
                    # ... e não é parede ... e não foi visitado
                    if (nx, ny) not in self.obstaculos and (nx, ny) not in visitados:
                        visitados.add((nx, ny))
                        fila.append((nx, ny))
                        
        return False # Esgotou todas as opções e não chegou à saída

    def atualizacao(self):
        pass 

    def agir(self, accao, agente):
        x, y = agente.posicao
        
        # Traduzir Ação
        dx, dy = 0, 0
        if accao in ['N', 'CIMA']: dy = -1
        elif accao in ['S', 'BAIXO']: dy = 1
        elif accao in ['O', 'ESQUERDA']: dx = -1
        elif accao in ['E', 'DIREITA']: dx = 1
        
        nx, ny = x + dx, y + dy
        
        # 1. Limites
        if not (0 <= nx < self.largura and 0 <= ny < self.altura):
            return -0.5, False 
            
        # 2. Obstáculos
        if (nx, ny) in self.obstaculos:
            return -0.5, False 
        
        # 3. Mover
        agente.posicao = (nx, ny)
        
        # 4. Vitória
        if agente.posicao == self.saida_pos:
            self.objetivo_alcancado = True
            return 20.0, True 
            
        return -0.1, False
    
    def estado_global(self):
        return f"Labirinto Validado ({len(self.obstaculos)} paredes)"