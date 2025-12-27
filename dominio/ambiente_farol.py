from core.ambiente import Ambiente

class AmbienteFarol(Ambiente):
    def __init__(self, largura, altura):
        super().__init__(largura, altura)
        self.posicao_farol = (largura - 1, altura - 1)
        self.objetivo_alcancado = False

    def agir(self, accao, agente):
        agente.actuador.executar(accao, agente, self)
        
        if agente.posicao == self.posicao_farol:
            self.objetivo_alcancado = True
            return 10.0, True
        
        return -0.1, False

    def estado_global(self):
        grelha = [[' . ' for _ in range(self.largura)] for _ in range(self.altura)]
        fx, fy = self.posicao_farol
        grelha[fy][fx] = ' F '
        
        for ag in self.agentes:
            ax, ay = ag.posicao
            marcador = ' A ' 
            if (ax, ay) == (fx, fy): marcador = ' # '
            grelha[ay][ax] = marcador
            
        return "\n".join(["".join(linha) for linha in grelha])
    
    def atualizacao(self):
        pass # no Farol o ambiente é estático, por isso não faz nada, mas cumpre a interface.