from core.sensor import Sensor

class SensorPosicao(Sensor):
    """Devolve as coordenadas (x, y) do agente."""
    def detetar(self, ambiente, agente):
        return {"x": agente.posicao[0], "y": agente.posicao[1]}
