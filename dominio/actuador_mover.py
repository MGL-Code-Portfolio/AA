from core.actuador import Actuador

class ActuadorMover(Actuador):
    def executar(self, accao, agente, ambiente):
        x, y = agente.posicao
        
        if accao == 'N': y -= 1
        elif accao == 'S': y += 1
        elif accao == 'O': x -= 1
        elif accao == 'E': x += 1
        
        # Validar limites
        x = max(0, min(x, ambiente.largura - 1))
        y = max(0, min(y, ambiente.altura - 1))
        
        agente.posicao = (x, y)