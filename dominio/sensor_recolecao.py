import math
from core.sensor import Sensor

class SensorVisaoRecurso(Sensor):
    
    def detetar(self, ambiente, agente):
        x, y = agente.posicao
        tem_recurso = getattr(agente, 'tem_recurso', False)
        
        target_x, target_y = x, y
        
        if tem_recurso:
            # obbjetivo -> ir para o Ninho
            target_x, target_y = ambiente.ninho_pos
        else:
            # ir para o recurso mais próximo
            if hasattr(ambiente, 'recursos') and ambiente.recursos:
                # Encontrar o recurso com menor distância Manhattan
                recurso_mais_perto = min(
                    ambiente.recursos, 
                    key=lambda r: abs(r[0]-x) + abs(r[1]-y)
                )
                target_x, target_y = recurso_mais_perto
            else:
                return {"dir_x": 0, "dir_y": 0}

        # Calcular Direção Normalizada (-1, 0, 1)
        dx = 1 if target_x > x else (-1 if target_x < x else 0)
        dy = 1 if target_y > y else (-1 if target_y < y else 0)
        
        return {"dir_x": dx, "dir_y": dy}
    

class SensorEstadoInterno(Sensor): # indica se o agente está a carregar um recurso.
    def detetar(self, ambiente, agente):
        tem_recurso = getattr(agente, 'tem_recurso', False)
        return {"tem_recurso": int(tem_recurso)}