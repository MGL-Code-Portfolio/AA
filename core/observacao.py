from typing import Dict, Any

class Observacao:
    #encapsula os dados observados pelo agente
    def __init__(self, dados: Dict[str, Any]):
        self.dados = dados
    
    def __hash__(self):
        return hash(tuple(sorted(self.dados.items())))
    
    def __eq__(self, other):
        return self.dados == other.dados
    
    def get(self, key, default=None):
        return self.dados.get(key, default)