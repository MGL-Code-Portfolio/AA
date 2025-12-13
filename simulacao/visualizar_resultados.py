import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_curva_aprendizagem(ficheiro_csv='resultados_treino.csv'):
    
    if not os.path.exists(ficheiro_csv):
        print(f"Erro: O ficheiro '{ficheiro_csv}' não foi encontrado.")
        print("Por favor, execute primeiro uma simulação em modo de treino para gerar o ficheiro.")
        return

    dados = pd.read_csv(ficheiro_csv)

   
    janela_media_movel = max(1, len(dados) // 20) # Janela de 5% do total de episódios
    dados['RecompensaMM'] = dados['Recompensa'].rolling(window=janela_media_movel, min_periods=1).mean()

    plt.figure(figsize=(12, 7))

    plt.plot(dados['Episodio'], dados['Recompensa'], label='Recompensa por Episódio', color='lightblue', alpha=0.5)

    plt.plot(dados['Episodio'], dados['RecompensaMM'], label=f'Tendência', color='blue', linewidth=2)

    plt.title('Curva de Aprendizagem do Agente (Q-Learning)', fontsize=16)
    plt.xlabel('Episódio de Treino', fontsize=12)
    plt.ylabel('Recompensa Acumulada', fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()

    nome_grafico = 'curva_aprendizagem_recompensa.png'
    plt.savefig(nome_grafico)
    print(f"\nGráfico da curva de aprendizagem salvo como '{nome_grafico}'")

if __name__ == "__main__":
    nome_ficheiro = input("Insira o nome do ficheiro CSV para analisar (default: resultados_treino.csv): ") or "resultados_treino.csv"
    plot_curva_aprendizagem(nome_ficheiro)