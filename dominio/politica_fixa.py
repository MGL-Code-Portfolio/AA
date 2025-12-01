from core.politica import Politica

class PoliticaFixa(Politica):
    """
    Estratégia Gulosa (Greedy).
    Move-se na direção do objetivo baseada nos sensores 'dir_x' e 'dir_y'.
    """
    def __init__(self):
        pass

    def decidir(self, observacao, agente):
        # Tenta obter dados de qualquer sensor que dê direção (Farol ou Recurso)
        # O .get(..., 0) evita erro se o sensor não existir
        dx = observacao.get("dir_x", 0) 
        dy = observacao.get("dir_y", 0)
        
        # Prioriza eixo Y (Cima/Baixo)
        if dy == -1: return 'N' # O alvo está para cima
        if dy == 1:  return 'S' # O alvo está para baixo
        
        # Se Y estiver alinhado, move no eixo X
        if dx == -1: return 'O' # O alvo está para a esquerda
        if dx == 1:  return 'E' # O alvo está para a direita
        
        # Se chegou ou não sabe, mantém a posição (ou explora)
        return 'N' 

    def atualizar(self, *args):
        pass