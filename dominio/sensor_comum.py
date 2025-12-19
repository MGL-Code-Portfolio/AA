from core.sensor import Sensor

class SensorPosicao(Sensor): #cordenadas x e y do agente no ambiente
    def detetar(self, ambiente, agente):
        return {"x": agente.posicao[0], "y": agente.posicao[1]}
