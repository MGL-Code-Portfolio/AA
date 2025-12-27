from core.ambiente import Ambiente
import random
from collections import deque # usado para o algoritmo de busca (BFS)

class AmbienteLabirinto(Ambiente):
    def __init__(self, largura, altura, densidade_paredes=0.25, seed=42):
        super().__init__(largura, altura)
        
        self.rng = random.Random(seed)
        self.inicio_pos = (0, 0)
        self.saida_pos = (largura - 1, altura - 1)
        self.obstaculos = set()
        self.densidade = densidade_paredes
        self.objetivo_alcancado = False
        
        # garante que o mapa gerado tem solução
        self.gerar_obstaculos_validos()

    def gerar_obstaculos_validos(self):
        max_tentativas = 100
        
        for _ in range(max_tentativas):
            self.obstaculos.clear()
            self._preencher_obstaculos_aleatorios()
            
            # se existir um caminho valido, aceitamos este mapa
            if self.existe_caminho():
                return 


    def _preencher_obstaculos_aleatorios(self):
        """Espalha obstáculos, protegendo apenas o início e o fim."""
        for x in range(self.largura):
            for y in range(self.altura):
                # nunca colocar parede no início ou no fim
                if (x, y) == self.inicio_pos or (x, y) == self.saida_pos:
                    continue
                
                if self.rng.random() < self.densidade:
                    self.obstaculos.add((x, y))

    def existe_caminho(self): #bfs para verificar se há caminho do inicio ao fim
        fila = deque([self.inicio_pos])
        visitados = {self.inicio_pos}
        
        while fila:
            x, y = fila.popleft()
            
            if (x, y) == self.saida_pos:
                return True # caminho encontrado
            
            vizinhos = [
                (x, y-1), (x, y+1), (x-1, y), (x+1, y)
            ]
            
            for nx, ny in vizinhos:
                # se dentro dos limites
                if 0 <= nx < self.largura and 0 <= ny < self.altura:
                    # nao pode ser parede e nao pode ter sido visitado
                    if (nx, ny) not in self.obstaculos and (nx, ny) not in visitados:
                        visitados.add((nx, ny))
                        fila.append((nx, ny))
                        
        return False 

    def reset(self):
        """Reseta o ambiente e a posição dos agentes para o início."""
        for agente in self.agentes:
            agente.posicao = self.inicio_pos
            agente.reset_stats()
        self.objetivo_alcancado = False

    def atualizacao(self):
        pass 

    def agir(self, accao, agente):
        posicao_anterior = agente.posicao[:] # cria uma cópia da tupla
        
        #delegar o movimento ao atuador do agente
        if agente.actuador:
            agente.actuador.executar(accao, agente, self)
        
        #verificar se houve colisão (se a posição não mudou)
        if agente.posicao == posicao_anterior:
            # atuador não conseguiu mover (bateu em parede ou limite)
            #print(f"Agente {agente.id} colidiu com uma parede em {agente.posicao}!")
            return -0.5, False 
        
        #win
        if agente.posicao == self.saida_pos:
            self.objetivo_alcancado = True
            return 20.0, True 
            
        #custo de cada passo
        return -0.1, False
    
    def estado_global(self):
        return f"Labirinto Validado ({len(self.obstaculos)} paredes)"