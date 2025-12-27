from typing import List
from core.politica import Politica
from core.sensor import Sensor
from core.actuador import Actuador
from core.observacao import Observacao

class Agente:
    def __init__(self, id_agente, politica: Politica):
        self.id = id_agente
        self.politica = politica
        self.sensores: List[Sensor] = []
        self.actuador: Actuador = None
        self.posicao = (0, 0)
        
        # Aprendizagem
        self.recompensa_acumulada = 0.0
        self.ultimo_estado = None
        self.ultima_accao = None

        self.stats = {
            "colisoes": 0,
            "celulas_visitadas": set(), #da save nas cordenadas visitadas
            "passos_episodio": 0,
            "visitas_posicao": {} # Track visitation frequency: (x, y) -> count
        }

    def reset_stats(self):
        self.stats = {
            "colisoes": 0,
            "celulas_visitadas": set(),
            "passos_episodio": 0,
            "visitas_posicao": {}
        }
        self.recompensa_acumulada = 0
        if hasattr(self, 'tem_recurso'): self.tem_recurso = False

    def instala(self, sensor: Sensor):
        self.sensores.append(sensor)
        
    def set_actuador(self, actuador: Actuador):
        self.actuador = actuador

    def observacao(self, ambiente):
        dados_coletados = {}
        for sensor in self.sensores:
            dados_coletados.update(sensor.detetar(ambiente, self))
        return Observacao(dados_coletados)

    def age(self, ambiente):
        obs = self.observacao(ambiente)
        self.ultimo_estado = obs
        accao = self.politica.decidir(obs, self)
        self.ultima_accao = accao
        return accao

    def avaliacaoEstadoAtual(self, recompensa, ambiente):
        self.recompensa_acumulada += recompensa
        novo_estado = self.observacao(ambiente)
        self.politica.atualizar(self.ultimo_estado, self.ultima_accao, recompensa, novo_estado)
