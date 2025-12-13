from core.politica import Politica

class PoliticaFixa(Politica): #greedy policy para recoleção e farol
    def __init__(self):
        pass

    def decidir(self, observacao, agente):
        # tenta obter dados dos sensores (farol ou recurso)
        dx = observacao.get("dir_x", 0) 
        dy = observacao.get("dir_y", 0)
        
        if dy == -1: return 'N' 
        if dy == 1:  return 'S' 
        
        if dx == -1: return 'O' 
        if dx == 1:  return 'E' 
        
        return 'N' 

    def atualizar(self, *args):
        pass