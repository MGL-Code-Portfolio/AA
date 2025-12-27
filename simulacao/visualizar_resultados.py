import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os

def plot_curva_aprendizagem(nome_base, ficheiro_csv):
    
    if not os.path.exists(ficheiro_csv):
        print(f"Erro: O ficheiro '{ficheiro_csv}' não foi encontrado.")
        return

    dados = pd.read_csv(ficheiro_csv)

    janela_media_movel = max(1, len(dados) // 20)
    dados['RecompensaMM'] = dados['Recompensa'].rolling(window=janela_media_movel, min_periods=1).mean()

    plt.figure(figsize=(12, 7))
    plt.plot(dados['Episodio'], dados['Recompensa'], label='Recompensa por Episódio', color='lightblue', alpha=0.5)
    plt.plot(dados['Episodio'], dados['RecompensaMM'], label=f'Tendência', color='blue', linewidth=2)

    plt.title(f'Curva de Aprendizagem - {nome_base}', fontsize=16)
    plt.xlabel('Episódio de Treino', fontsize=12)
    plt.ylabel('Recompensa Acumulada', fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()

    nome_grafico = nome_base + "_curva_aprendizagem.png"
    plt.savefig(nome_grafico)
    plt.close()
    print(f"Gráfico da curva de aprendizagem salvo como '{nome_grafico}'")

def plot_comparacao_politicas(lista_csvs, nome_arquivo_saida="comparacao_politicas.png"):
    """
    Gera um gráfico comparativo das curvas de aprendizado (média móvel) de vários arquivos CSV.
    """
    plt.figure(figsize=(12, 8))

    for ficheiro in lista_csvs:
        if not os.path.exists(ficheiro): continue

        try:
            dados = pd.read_csv(ficheiro)
            if 'Recompensa' not in dados.columns: continue

            # Identificar nome da política pelo nome do arquivo
            # Ex: AmbienteFarol_QLearning_simulacao.csv -> QLearning
            nome_legenda = os.path.basename(ficheiro).replace("_simulacao.csv", "")

            janela = max(1, len(dados) // 20)
            media_movel = dados['Recompensa'].rolling(window=janela, min_periods=1).mean()

            plt.plot(dados['Episodio'], media_movel, label=nome_legenda, linewidth=2)
        except Exception as e:
            print(f"Erro ao processar {ficheiro}: {e}")

    plt.title('Comparação de Políticas (Tendência de Recompensa)', fontsize=16)
    plt.xlabel('Episódio', fontsize=12)
    plt.ylabel('Recompensa Média (Smoothed)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()

    plt.savefig(nome_arquivo_saida)
    plt.close()
    print(f"Gráfico comparativo salvo como '{nome_arquivo_saida}'")

def gerar_heatmap_exploracao(agente, largura, altura, nome_base):
    """
    Gera um heatmap baseado na densidade real de visitas do agente (visitas_posicao).
    """
    stats = getattr(agente, 'stats', None)
    if not stats or 'visitas_posicao' not in stats:
        print("Aviso: Agente sem estatísticas de visitas para heatmap.")
        return

    visitas = stats['visitas_posicao']

    # Criar matriz
    heatmap_data = [[0 for _ in range(largura)] for _ in range(altura)]

    max_visits = 0
    for (x, y), count in visitas.items():
        if 0 <= x < largura and 0 <= y < altura:
            heatmap_data[y][x] = count
            if count > max_visits: max_visits = count

    if max_visits == 0:
        print("Aviso: Nenhuma visita registrada para heatmap de exploração.")
        return

    plt.figure(figsize=(10, 8))
    # cmap 'hot' ou 'inferno' é bom para densidade
    im = plt.imshow(heatmap_data, cmap='inferno', interpolation='nearest', origin='upper')

    plt.colorbar(im, label='Frequência de Visitas')
    plt.title(f'Mapa de Calor de Exploração Real (Densidade) - Agente {agente.id}')
    plt.xlabel('X')
    plt.ylabel('Y')

    nome_arquivo = f"{nome_base}_heatmap_densidade.png"
    plt.savefig(nome_arquivo)
    plt.close()
    print(f"Heatmap de densidade salvo como '{nome_arquivo}'")

def gerar_heatmap_qtable(ambiente_nome, arquivo_qtable, largura, altura):
    """
    Gera um heatmap baseado nos valores máximos da Q-Table.
    """
    if not os.path.exists(arquivo_qtable):
        # print(f"Aviso: Ficheiro da Q-Table '{arquivo_qtable}' não encontrado. Heatmap ignorado.")
        return

    try:
        with open(arquivo_qtable, 'rb') as f:
            q_tabela = pickle.load(f)
    except Exception as e:
        print(f"Erro ao ler Q-Table: {e}")
        return

    heatmap_data = [[0.0 for _ in range(largura)] for _ in range(altura)]
    visitado = [[False for _ in range(largura)] for _ in range(altura)]

    for key_tuple, actions in q_tabela.items():
        x, y = -1, -1
        try:
            state_dict = dict(key_tuple)
            if 'x' in state_dict and 'y' in state_dict:
                x = state_dict['x']
                y = state_dict['y']
        except:
            continue

        if 0 <= x < largura and 0 <= y < altura:
            max_q = max(actions.values()) if actions else 0.0
            if max_q > heatmap_data[y][x] or not visitado[y][x]:
                heatmap_data[y][x] = max_q
                visitado[y][x] = True

    plt.figure(figsize=(10, 8))
    im = plt.imshow(heatmap_data, cmap='viridis', interpolation='nearest', origin='upper')

    plt.colorbar(im, label='Max Q-Value')
    plt.title(f'Mapa de Calor de Valores Q - {ambiente_nome}')
    plt.xlabel('X (Largura)')
    plt.ylabel('Y (Altura)')

    nome_arquivo = f"{ambiente_nome}_heatmap.png"
    plt.savefig(nome_arquivo)
    plt.close()
    print(f"Heatmap Q-Table salvo como '{nome_arquivo}'")
