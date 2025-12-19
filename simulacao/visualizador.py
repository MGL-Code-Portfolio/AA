import os

class Visualizador:
    def renderizar(self, ambiente):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"--- Passo: {ambiente.passo_atual} ---")
        print(ambiente.estado_global())
        print("-" * 20)