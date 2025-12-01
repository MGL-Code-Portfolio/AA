from core.sensor import Sensor

class SensorPosicao(Sensor):
    """Devolve as coordenadas (x, y) do agente."""
    def detetar(self, ambiente, agente):
        return {"x": agente.posicao[0], "y": agente.posicao[1]}

class SensorEstadoInterno(Sensor):
    """Deteta se o agente está a carregar um recurso (para Recoleção)."""
    def detetar(self, ambiente, agente):
        # Verifica se o atributo existe, se não, assume False
        tem_recurso = getattr(agente, 'tem_recurso', False)
        return {"tem_recurso": int(tem_recurso)}