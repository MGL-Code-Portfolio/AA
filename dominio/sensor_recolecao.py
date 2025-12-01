import math
from core.sensor import Sensor

class SensorVisaoRecurso(Sensor):
    """
    Indica a direção do objetivo atual:
    - Se não tiver recurso: Aponta para o recurso mais próximo.
    - Se tiver recurso: Aponta para o ninho.
    """
    def detetar(self, ambiente, agente):
        x, y = agente.posicao
        tem_recurso = getattr(agente, 'tem_recurso', False)
        
        target_x, target_y = x, y
        
        if tem_recurso:
            # Objetivo: Ir para o Ninho
            target_x, target_y = ambiente.ninho_pos
        else:
            # Objetivo: Ir para o Recurso mais próximo
            if hasattr(ambiente, 'recursos') and ambiente.recursos:
                # Encontrar o recurso com menor distância Manhattan
                recurso_mais_perto = min(
                    ambiente.recursos, 
                    key=lambda r: abs(r[0]-x) + abs(r[1]-y)
                )
                target_x, target_y = recurso_mais_perto
            else:
                # Não há recursos? Fica quieto (ou explora aleatoriamente)
                return {"dir_x": 0, "dir_y": 0}

        # Calcular Direção Normalizada (-1, 0, 1)
        dx = 1 if target_x > x else (-1 if target_x < x else 0)
        dy = 1 if target_y > y else (-1 if target_y < y else 0)
        
        return {"dir_x": dx, "dir_y": dy}