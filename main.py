import time
import os
import random 

from core.agente import Agente
from simulacao.motor import MotorDeSimulacao
from simulacao.visualizador_gui import VisualizadorGUI
from simulacao.logger import Logger

from dominio.ambiente_farol import AmbienteFarol
from dominio.ambiente_labirinto import AmbienteLabirinto
from dominio.ambiente_recolecao import AmbienteRecolecao

from dominio.actuador_mover import ActuadorMover
from dominio.politica_qlearning import PoliticaQlearning
from dominio.politica_fixa import PoliticaFixa           
from dominio.politica_aleatoria import PoliticaAleatoria 
from dominio.politica_novelty import PoliticaNovelty

from dominio.sensor_farol import SensorDireccaoFarol
from dominio.sensor_comum import SensorPosicao
from simulacao.visualizar_resultados import plot_curva_aprendizagem, gerar_heatmap_qtable, plot_comparacao_politicas, gerar_heatmap_exploracao
from dominio.sensor_recolecao import SensorEstadoInterno, SensorVisaoRecurso

def limpar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_configuracao():
    limpar_consola()
    print("="*60)
    print("   SIMULADOR DE SISTEMAS MULTI-AGENTE (SMA)")
    print("="*60)
    
    # 1. Ambiente
    print("\n[1] ESCOLHA O CENÁRIO:")
    print("   1. Farol (Métricas: Passos, Sucesso)")
    print("   2. Labirinto (Métricas: Saída, Células Visitadas)")
    print("   3. Recoleção (Métricas: Recursos, Eficiência, Colisões)")
    escolha_amb = input("   >>> Opção (1-3): ")
    
    # 2. Política
    print("\n[2] ESCOLHA A INTELIGÊNCIA:")
    print("   1. Q-Learning")
    print("   2. Política Fixa")
    print("   3. Aleatória")
    print("   4. Novelty Search")
    escolha_pol = input("   >>> Opção (1-4): ")

    #Parâmetros do Mundo
    try:
        largura = int(input("\n   >>> Largura (default 6): ") or 6)
        altura = int(input("   >>> Altura (default 6): ") or 6)
        n_agentes = int(input("   >>> Nº de Agentes (default 1): ") or 1)
    except:
        largura, altura, n_agentes = 6, 6, 1

    # Modo de Execução
    print("\n[4] MODO DE EXECUÇÃO:")
    print("   1. Treino Completo + Teste Visual")
    print("   2. Apenas Treino (Gera CSV rápido e sai)")
    print("   3. Apenas Teste Visual (Sem treino prévio)")
    modo_exec = input("   >>> Opção (1-3): ")

    # 5. Episódios de Treino, só pergunta se for necessário treinar
    episodios = 0
    if modo_exec in ['1', '2'] and escolha_pol in ['1', '4']:
        try:
            episodios = int(input("\n   >>> Nº Episódios Treino (default 200): ") or 200)
        except: episodios = 200
    
    return escolha_amb, escolha_pol, largura, altura, episodios, n_agentes, modo_exec

def criar_ambiente_e_agente(tipo_amb, tipo_pol, largura, altura, n_agentes):
    ambiente = None
    
    # setup Ambiente
    if tipo_amb == '1':
        ambiente = AmbienteFarol(largura, altura)
    elif tipo_amb == '2':
        ambiente = AmbienteLabirinto(largura, altura)
        ambiente.posicao_farol = ambiente.saida_pos 
    elif tipo_amb == '3':
        n_recursos = max(5, n_agentes * 2)
        ambiente = AmbienteRecolecao(largura, altura, num_recursos=n_recursos)
    else: exit()

    # loop para criar Agentes
    for i in range(n_agentes):
        sensores = []
        # Generalização: Remover SensorPosicao para forçar uso de sensores relativos

        if tipo_amb == '1':
            sensores.append(SensorDireccaoFarol())
            sensores.append(SensorPosicao()) # REMOVIDO para generalização
        elif tipo_amb == '2':
            sensores.append(SensorPosicao()) # REMOVIDO para generalização
            sensores.append(SensorDireccaoFarol()) # Adicionado para navegação relativa
        elif tipo_amb == '3':
            sensores.append(SensorPosicao()) # REMOVIDO para generalização
            sensores.append(SensorEstadoInterno())
            sensores.append(SensorVisaoRecurso())

        # FIX: Novelty Search precisa de posição (state aliasing)
        if tipo_pol == '4':
            sensores.append(SensorPosicao())

        accoes = ['N', 'S', 'E', 'O']
        if tipo_pol == '1': politica = PoliticaQlearning(accoes_possiveis=accoes)
        elif tipo_pol == '2': politica = PoliticaFixa()
        elif tipo_pol == '3': politica = PoliticaAleatoria(accoes_possiveis=accoes)
        elif tipo_pol == '4': politica = PoliticaNovelty(accoes_possiveis=accoes)
        else: politica = PoliticaAleatoria(accoes_possiveis=accoes)

        agente = Agente(id_agente=i+1, politica=politica)
        for s in sensores: agente.instala(s)
        agente.set_actuador(ActuadorMover())
        
        pos_ini = (0, 0)
        if tipo_amb == '3':
            pos_ini = (random.randint(0, largura-1), random.randint(0, altura-1))

        ambiente.adicionar_agente(agente, pos_inicial=pos_ini)
        
    return ambiente

def apresentar_metricas_finais(historico_testes, tipo_amb):
    num_testes = len(historico_testes)
    if num_testes == 0: return

    total_recompensa = sum(h['recompensa_media_grupo'] for h in historico_testes)
    total_sucessos = sum(1 for h in historico_testes if h['sucesso_global'])
    total_passos = sum(h['passos'] for h in historico_testes)
    
    print("\n" + "="*50)
    print("   RELATÓRIO FINAL DE DESEMPENHO (MÉTRICAS)")
    print("="*50)
    
    if tipo_amb == '1':
        print(f"-> CENÁRIO: FAROL")
        print(f"   • Taxa de Sucesso (Grupo): {(total_sucessos/num_testes)*100:.1f}%")
        print(f"   • Recompensa Média:        {total_recompensa/num_testes:.2f}")
        print(f"   • Passos Médios:           {total_passos/num_testes:.1f}")
    elif tipo_amb == '2':
        media_visitadas = sum(h['celulas_visitadas_total'] for h in historico_testes) / num_testes
        print(f"-> CENÁRIO: LABIRINTO")
        print(f"   • Taxa de Sucesso:         {(total_sucessos/num_testes)*100:.1f}%")
        print(f"   • Passos até Saída:        {total_passos/num_testes:.1f}")
        print(f"   • Total Células Visitadas: {media_visitadas:.1f}")
    elif tipo_amb == '3':
        total_recursos = sum(h['recursos_recolhidos_total'] for h in historico_testes)
        total_colisoes = sum(h['colisoes_total'] for h in historico_testes)
        eficiencia = total_recursos / total_passos if total_passos > 0 else 0
        print(f"-> CENÁRIO: RECOLEÇÃO")
        print(f"   • Recursos Recolhidos:     {total_recursos}")
        print(f"   • Média por Episódio:      {total_recursos/num_testes:.1f}")
        print(f"   • Colisões (Total Grupo):  {total_colisoes/num_testes:.1f}")
        print(f"   • Eficiência:              {eficiencia:.4f} rec/passo")
    
    print("="*50 + "\n")

def main():
    tipo_amb, tipo_pol, w, h, eps, n_agentes, modo_exec = menu_configuracao()
    
    env = criar_ambiente_e_agente(tipo_amb, tipo_pol, w, h, n_agentes)
    gui = VisualizadorGUI(w, h)
    motor = MotorDeSimulacao(env, visualizador=gui)

    nome_amb = env.__class__.__name__
    nome_pol = "QLearning"
    if tipo_pol == '4': nome_pol = "Novelty"
    elif tipo_pol == '3': nome_pol = "Aleatorio"
    elif tipo_pol == '2': nome_pol = "Fixo"

    # Definir pasta de saída baseada no ambiente
    if "Farol" in nome_amb: folder = "farol"
    elif "Labirinto" in nome_amb: folder = "labirinto"
    elif "Recolecao" in nome_amb: folder = "recolecao"
    else: folder = "outros"

    if not os.path.exists(folder):
        os.makedirs(folder)

    csv_filename = os.path.join(folder, f"{nome_amb}_{nome_pol}_simulacao.csv")
    logger = Logger(csv_filename)

    # CARREGAR Q-TABLE SE EXISTIR E FOR Q-LEARNING OU NOVELTY
    # Novelty herda de QLearning, então pode usar persistência também
    if tipo_pol in ['1', '4']:
        # Verifica se existe pelo menos um ficheiro para o primeiro agente
        exemplo_ficheiro = os.path.join(folder, f"qtable_{nome_amb}_{nome_pol}_ag1.pkl")
        carregar = False
        if os.path.exists(exemplo_ficheiro):
             resp = input(f"\n[PERSISTÊNCIA] Encontrada tabela salva ({exemplo_ficheiro}). Deseja carregar? (s/n): ")
             if resp.lower() == 's':
                 carregar = True

        if carregar:
            for ag in env.agentes:
                nome_fich = os.path.join(folder, f"qtable_{nome_amb}_{nome_pol}_ag{ag.id}.pkl")
                if hasattr(ag.politica, 'carregar_tabela'):
                    ag.politica.carregar_tabela(nome_fich)

    # auxiliares para decidir fases
    executar_treino = (modo_exec in ['1', '2']) and (tipo_pol in ['1', '4'])
    executar_teste = (modo_exec in ['1', '3'])

    #  FASE 1: APRENDIZAGEM 
    if executar_treino: 
        print(f"\n[MODO APRENDIZAGEM] A executar {eps} episódios com {n_agentes} agentes ({nome_pol})...")
        
        for ag in env.agentes:
            ag.politica.modo_treino = True
            
        start = time.time()
        for i in range(1, eps + 1):
            motor.executa_episodio(max_passos=100, visual=False)
            
            sucesso = getattr(env, 'objetivo_alcancado', False)
            if tipo_amb == '3': sucesso = (env.pontuacao_total > 0)
            
            recompensa_media = sum(a.recompensa_acumulada for a in env.agentes) / n_agentes
            logger.registar_episodio(i, env.passo_atual, recompensa_media, sucesso)
            
            if i % (max(1, eps//10)) == 0:
                print(f"   Progresso: {i}/{eps} | R (Média): {recompensa_media:.1f}")

        print(f"[MODO APRENDIZAGEM] Concluído em {time.time()-start:.2f}s")
        csv_exportado = logger.exportar_csv()

        # GUARDAR Q-TABLE NO FIM DO TREINO
        print("\n[PERSISTÊNCIA] A guardar tabelas Q...")
        for ag in env.agentes:
            if hasattr(ag.politica, 'guardar_tabela'):
                nome_fich = os.path.join(folder, f"qtable_{nome_amb}_{nome_pol}_ag{ag.id}.pkl")
                ag.politica.guardar_tabela(nome_fich)

    else:
        if tipo_pol in ['1', '4'] and modo_exec == '3':
            print("\n[AVISO] A executar Learning sem treino prévio. O comportamento será aleatório (ou carregado).")

    # FASE 2: TESTE E AVALIAÇÃO
    if executar_teste:
        if executar_treino: # só pede pausa se tiver havido treino antes
            input("\n[PRONTO] Pressiona ENTER para iniciar a AVALIAÇÃO (Visual)...")
        else:
            print("\n[MODO TESTE] A iniciar visualização imediata...")

        # desativar treino para TODOS
        for ag in env.agentes:
            if hasattr(ag.politica, 'modo_treino'):
                ag.politica.modo_treino = False
                if hasattr(ag.politica, 'epsilon'):
                     ag.politica.epsilon = 0.0 # desativar exploração

        historico_testes = []
        num_testes = 1 # Para teste visual basta 1 ou poucos
        if modo_exec == '3' and not executar_treino: num_testes = 5
        
        print(f"A executar {num_testes} episódios de teste...")
        
        for i in range(num_testes):
            motor.executa_episodio(max_passos=60, visual=True, delay=0.1)
            
            sucesso_ep = getattr(env, 'objetivo_alcancado', False)
            recursos = getattr(env, 'pontuacao_total', 0)
            if tipo_amb == '3' and recursos > 0: sucesso_ep = True
            
            # dados agregados
            recompensa_media = sum(a.recompensa_acumulada for a in env.agentes) / n_agentes
            total_celulas = sum(len(a.stats['celulas_visitadas']) for a in env.agentes)
            total_colisoes = sum(a.stats['colisoes'] for a in env.agentes)

            dados_teste = {
                'sucesso_global': sucesso_ep,
                'recompensa_media_grupo': recompensa_media,
                'passos': env.passo_atual,
                'celulas_visitadas_total': total_celulas,
                'colisoes_total': total_colisoes,
                'recursos_recolhidos_total': recursos
            }
            historico_testes.append(dados_teste)
            
            status = "Sucesso" if sucesso_ep else "Falha"
            print(f"   Episódio {i+1}: {status} (R Média: {recompensa_media:.1f})")
            time.sleep(0.5)

        apresentar_metricas_finais(historico_testes, tipo_amb)
    
    # FASE 3: VISUALIZAÇÃO DOS RESULTADOS DE TREINO 
    if executar_treino or (tipo_pol in ['1', '4'] and carregar):
        print("\n[VISUALIZAÇÃO] A gerar gráficos...")
        if executar_treino:
            # Gráfico de curva de aprendizagem
            # Usa o nome do arquivo que foi realmente exportado (pode ser backup)
            arquivo_para_plot = csv_exportado if csv_exportado else csv_filename
            plot_curva_aprendizagem(os.path.join(folder, f"{nome_amb}_{nome_pol}"), arquivo_para_plot)

            # Tenta plotar comparação se houver outros CSVs
            # Ex: Procura csvs padrão na pasta
            lista_csvs = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('_simulacao.csv') and nome_amb in f]
            if len(lista_csvs) > 1:
                plot_comparacao_politicas(lista_csvs, nome_arquivo_saida=os.path.join(folder, "comparacao_politicas.png"))

        # Gerar Heatmaps para os agentes Q-Learning / Novelty
        if tipo_pol in ['1', '4']:
            for ag in env.agentes:
                # Heatmap Q-Table
                nome_fich = os.path.join(folder, f"qtable_{nome_amb}_{nome_pol}_ag{ag.id}.pkl")
                nome_amb_agente = os.path.join(folder, f"{nome_amb}_{nome_pol}_Agente{ag.id}")
                gerar_heatmap_qtable(nome_amb_agente, nome_fich, w, h)

                # Heatmap Exploração Real (Densidade)
                gerar_heatmap_exploracao(ag, w, h, f"{nome_amb_agente}_exploracao")

    print("\nSimulação Terminada.")

if __name__ == "__main__":
    main()
