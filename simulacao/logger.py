import csv
import os

class Logger:
    def __init__(self, nome_ficheiro="dados_simulacao.csv"):
        self.nome_ficheiro = nome_ficheiro
        self.historico = []
        self.limpar_ficheiro_anterior()

    def limpar_ficheiro_anterior(self):
        if os.path.exists(self.nome_ficheiro):
            os.remove(self.nome_ficheiro)

    def registar_episodio(self, episodio, passos, recompensa, sucesso):
        dados = {
            "Episodio": episodio,
            "Passos": passos,
            "Recompensa": round(recompensa, 4),
            "Sucesso": 1 if sucesso else 0
        }
        self.historico.append(dados)

    def exportar_csv(self):
        if not self.historico:
            return
        
        chaves = self.historico[0].keys()
        
        try:
            with open(self.nome_ficheiro, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=chaves)
                writer.writeheader()
                writer.writerows(self.historico)
            print(f"\n[LOGGER] Dados exportados com sucesso para: {self.nome_ficheiro}")
        except IOError as e:
            print(f"[LOGGER] Erro ao gravar CSV: {e}")