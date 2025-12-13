from core.sensor import Sensor

class SensorDireccaoFarol(Sensor):
    def detetar(self, ambiente, agente):
        ax, ay = agente.posicao
        # O ambiente TEM de ter self.posicao_farol
        if hasattr(ambiente, 'posicao_farol'):
            fx, fy = ambiente.posicao_farol
        else:
            return {"dir_x": 0, "dir_y": 0}
        
        dx = 1 if fx > ax else (-1 if fx < ax else 0)
        dy = 1 if fy > ay else (-1 if fy < ay else 0)
        
        return {"dir_x": dx, "dir_y": dy}