import csv
import os
import time

class Logger:
    def __init__(self, nome_ficheiro):
        self.nome_ficheiro = nome_ficheiro
        self.historico = []
        # Em vez de apagar, apenas testamos se temos acesso
        self._verificar_acesso()

    def _verificar_acesso(self):
        """Verifica se o ficheiro está bloqueado antes de começar o treino."""
        if os.path.exists(self.nome_ficheiro):
            try:
                # Tenta abrir para acrescentar (append), o que testa permissões sem apagar
                with open(self.nome_ficheiro, 'a'):
                    pass
            except IOError:
                # Se falhar, gera um nome único com timestamp para não perder os dados
                timestamp = int(time.time())
                novo_nome = f"{timestamp}_{self.nome_ficheiro}"
                print(f"[LOGGER] Aviso: Ficheiro original bloqueado. A usar: {novo_nome}")
                self.nome_ficheiro = novo_nome

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
            return None
        
        chaves = self.historico[0].keys()
        
        try:
            # O modo 'w' já limpa o ficheiro automaticamente ao abrir
            with open(self.nome_ficheiro, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=chaves)
                writer.writeheader()
                writer.writerows(self.historico)
            print(f"\n[LOGGER] Dados exportados para: {self.nome_ficheiro}")
            return self.nome_ficheiro
        except IOError as e:
            print(f"[LOGGER] Erro ao gravar CSV: {e}")
            return None