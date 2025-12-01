from core.ambiente import Ambiente
import random

class AmbienteRecolecao(Ambiente):
    def __init__(self, largura, altura, num_recursos=5):
        super().__init__(largura, altura)
        self.ninho_pos = (0, 0) # Ninho no canto superior esquerdo
        self.num_recursos_inicial = num_recursos
        self.recursos = set()
        self.pontuacao_total = 0
        self._gerar_recursos()

    def _gerar_recursos(self):
        """Gera recursos em posições aleatórias (sem sobrepor ninho)"""
        while len(self.recursos) < self.num_recursos_inicial:
            rx = random.randint(0, self.largura - 1)
            ry = random.randint(0, self.altura - 1)
            if (rx, ry) != self.ninho_pos:
                self.recursos.add((rx, ry))

    def atualizacao(self):
        # Opcional: Recursos poderiam "renascer" aqui
        pass

    def agir(self, accao, agente):
        # Inicializa estado do agente se não existir
        if not hasattr(agente, 'tem_recurso'):
            agente.tem_recurso = False

        recompensa = -0.1 # Custo de energia por passo

        # --- Lógica de Movimento ---
        x, y = agente.posicao
        nx, ny = x, y
        if accao == 'N': ny -= 1
        elif accao == 'S': ny += 1
        elif accao == 'O': nx -= 1
        elif accao == 'E': nx += 1
        
        # Limites
        nx = max(0, min(nx, self.largura - 1))
        ny = max(0, min(ny, self.altura - 1))
        agente.posicao = (nx, ny)

        # --- Lógica de Recoleção ---
        
        # 1. Apanhar Recurso (Se estiver em cima e não tiver carga)
        if (nx, ny) in self.recursos and not agente.tem_recurso:
            agente.tem_recurso = True
            self.recursos.remove((nx, ny))
            recompensa = 5.0 # Recompensa por apanhar
            # print(f"Agente {agente.id} apanhou recurso!")

        # 2. Entregar no Ninho (Se estiver no ninho e tiver carga)
        elif (nx, ny) == self.ninho_pos and agente.tem_recurso:
            agente.tem_recurso = False
            self.pontuacao_total += 1
            recompensa = 20.0 # Grande recompensa por entregar
            # print(f"Agente {agente.id} entregou recurso!")
            
            # (Opcional) Faz respawn de recurso para o ciclo continuar
            self._gerar_recursos()

        return recompensa, False # Nunca "termina" realmente, é contínuo até timeout

    def estado_global(self):
        return f"Recursos: {len(self.recursos)} | Entregues: {self.pontuacao_total}"