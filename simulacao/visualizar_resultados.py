import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os

def plot_curva_aprendizagem(ambiente, ficheiro_csv):
    
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

    nome_grafico = ambiente.replace(" ", "_") + "_curva_aprendizagem.png"
    plt.savefig(nome_grafico)
    print(f"\nGráfico da curva de aprendizagem salvo como '{nome_grafico}'")

def gerar_heatmap_qtable(ambiente_nome, arquivo_qtable, largura, altura):
    """
    Gera um heatmap baseado nos valores máximos da Q-Table para cada posição (x, y).
    Assume que a chave da Q-Table contém tuplas com itens ('x', val) e ('y', val).
    """
    if not os.path.exists(arquivo_qtable):
        print(f"Aviso: Ficheiro da Q-Table '{arquivo_qtable}' não encontrado. Heatmap ignorado.")
        return

    try:
        with open(arquivo_qtable, 'rb') as f:
            q_tabela = pickle.load(f)
    except Exception as e:
        print(f"Erro ao ler Q-Table: {e}")
        return

    # Inicializar matriz de valores
    # Usando listas de listas já que numpy pode não estar disponível diretamente no escopo global
    # mas matplotlib consegue plotar listas de listas.
    heatmap_data = [[0.0 for _ in range(largura)] for _ in range(altura)]
    visitado = [[False for _ in range(largura)] for _ in range(altura)]

    # Iterar sobre a tabela
    for key_tuple, actions in q_tabela.items():
        # A chave é uma tupla de itens, ex: (('dir_x', 0), ('x', 1), ('y', 2))
        # Precisamos extrair x e y.
        x, y = -1, -1

        # Converter tupla de pares em dict para busca fácil
        try:
            state_dict = dict(key_tuple)
            if 'x' in state_dict and 'y' in state_dict:
                x = state_dict['x']
                y = state_dict['y']
        except:
            continue

        # Validar coordenadas
        if 0 <= x < largura and 0 <= y < altura:
            # Calcular o valor máximo Q para este estado
            max_q = max(actions.values()) if actions else 0.0

            # Se já visitamos esta célula (outra combinação de sensores para o mesmo x,y),
            # podemos querer a média ou o máximo global. Vamos usar o Máximo Global para representar "o melhor que se sabe".
            if max_q > heatmap_data[y][x] or not visitado[y][x]:
                heatmap_data[y][x] = max_q
                visitado[y][x] = True

    # Plotar Heatmap
    plt.figure(figsize=(10, 8))
    im = plt.imshow(heatmap_data, cmap='viridis', interpolation='nearest', origin='upper') # origin upper combina com matrizes (0,0 no topo)
    # Nota: Em muitos ambientes 2D, (0,0) é topo-esquerda ou baixo-esquerda.
    # Assumindo sistema de coordenadas de matriz (y=linha, x=coluna).

    plt.colorbar(im, label='Max Q-Value')
    plt.title(f'Mapa de Calor de Valores Q - {ambiente_nome}')
    plt.xlabel('X (Largura)')
    plt.ylabel('Y (Altura)')

    # Anotações (opcional, pode poluir se for grande)
    if largura <= 20 and altura <= 20:
        for i in range(altura):
            for j in range(largura):
                val = heatmap_data[i][j]
                if val != 0:
                    plt.text(j, i, f'{val:.1f}', ha='center', va='center', color='w', fontsize=8)

    nome_arquivo = f"{ambiente_nome}_heatmap.png"
    plt.savefig(nome_arquivo)
    plt.close()
    print(f"Heatmap salvo como '{nome_arquivo}'")
