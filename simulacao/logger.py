import csv
import os

class Logger:
    def __init__(self, nome_ficheiro):
        self.nome_ficheiro = nome_ficheiro
        self.historico = []
        self.limpar_ficheiro_anterior()

    def limpar_ficheiro_anterior(self):
        if os.path.exists(self.nome_ficheiro):
            try:
                os.remove(self.nome_ficheiro)
            except OSError as e:
                print(f"[LOGGER] Aviso: Não foi possível limpar o ficheiro anterior '{self.nome_ficheiro}': {e}")

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
            print(f"[LOGGER] Erro ao gravar CSV '{self.nome_ficheiro}': {e}")
            # Tentar salvar com outro nome
            novo_nome = "backup_" + self.nome_ficheiro
            try:
                 with open(novo_nome, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=chaves)
                    writer.writeheader()
                    writer.writerows(self.historico)
                 print(f"[LOGGER] Dados salvos em ficheiro alternativo: {novo_nome}")
            except IOError as e2:
                 print(f"[LOGGER] CRÍTICO: Não foi possível salvar dados nem no backup: {e2}")