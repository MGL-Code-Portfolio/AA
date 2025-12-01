from core.actuador import Actuador

class ActuadorMover(Actuador):
    def executar(self, accao, agente, ambiente):
        x, y = agente.posicao
        
        dx, dy = 0, 0
        
        if accao in ['N', 'CIMA', 'MOVER_CIMA']: dy = -1
        elif accao in ['S', 'BAIXO', 'MOVER_BAIXO']: dy = 1
        elif accao in ['O', 'ESQUERDA', 'MOVER_ESQUERDA']: dx = -1
        elif accao in ['E', 'DIREITA', 'MOVER_DIREITA']: dx = 1
        
        nx, ny = x + dx, y + dy
        
        # Validar limites do ambiente (Grelha)
        if 0 <= nx < ambiente.largura and 0 <= ny < ambiente.altura:
            # Validar Obstáculos (se o ambiente tiver essa info)
            if hasattr(ambiente, 'obstaculos') and (nx, ny) in ambiente.obstaculos:
                return # Bateu na parede, não move
            
            # Movimento válido
            agente.posicao = (nx, ny)