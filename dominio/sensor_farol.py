from core.sensor import Sensor

class SensorDireccaoFarol(Sensor):
    def detetar(self, ambiente, agente):
        ax, ay = agente.posicao
        # Nota: Assume-se que o ambiente tem a propriedade 'posicao_farol'
        fx, fy = ambiente.posicao_farol
        
        dx = 1 if fx > ax else (-1 if fx < ax else 0)
        dy = 1 if fy > ay else (-1 if fy < ay else 0)
        
        return {"dir_x": dx, "dir_y": dy}