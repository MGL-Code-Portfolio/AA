from core.ambiente import Ambiente
import random

class AmbienteRecolecao(Ambiente):
    def __init__(self, largura, altura, num_recursos=5):
        super().__init__(largura, altura)
        self.ninho_pos = (0, 0) # ninho no canto superior esquerdo
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
        pass

    def agir(self, accao, agente):
        # Inicializa estado do agente se não existir
        if not hasattr(agente, 'tem_recurso'):
            agente.tem_recurso = False

        recompensa = -0.3 # Custo de energia por passo

        posicao_anterior = agente.posicao[:] # copia a posição




        #  lógica de Movimento 
        if agente.actuador:
            agente.actuador.executar(accao, agente, self)

        # Validação de Colisão 
        if agente.posicao == posicao_anterior:
            agente.stats['colisoes'] += 1
            return -1.0, False # penalização por colisão com limites

        # validação de Colisão com outros Agentes
        for outro_agente in self.agentes:
            if agente.id == outro_agente.id:
                continue # não verificar colisão consigo mesmo
            
            if agente.posicao == outro_agente.posicao:
                agente.posicao = posicao_anterior # reverte o movimento
                agente.stats['colisoes'] += 1
                outro_agente.stats['colisoes'] += 1 # o outro agente também colidiu
                return -1.0, False # penaliza o agente que se moveu


        # apanhar Recurso (Se estiver em cima e não tiver carga)
        if agente.posicao in self.recursos and not agente.tem_recurso:
            agente.tem_recurso = True
            self.recursos.remove(agente.posicao)
            recompensa = 5.0 # recompensa por apanhar
            #print(f"Agente {agente.id} apanhou recurso!") #usado para debug

        # entregar no Ninho (se estiver no ninho e tiver carga)
        elif agente.posicao == self.ninho_pos and agente.tem_recurso:
            agente.tem_recurso = False
            self.pontuacao_total += 1
            recompensa = 20.0 # grande recompensa por entregar
            #print(f"Agente {agente.id} entregou recurso!") #para debug
            
            self._gerar_recursos()

        return recompensa, False # Nnnca "termina" realmente, é contínuo até timeout

    def estado_global(self):
        return f"Recursos: {len(self.recursos)} | Entregues: {self.pontuacao_total}"