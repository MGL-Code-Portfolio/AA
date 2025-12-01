import time
import os

# --- Imports Core ---
from core.agente import Agente
from simulacao.motor import MotorDeSimulacao
from simulacao.visualizador_gui import VisualizadorGUI
from simulacao.logger import Logger

# --- Imports Ambientes ---
from dominio.ambiente_farol import AmbienteFarol
from dominio.ambiente_labirinto import AmbienteLabirinto
from dominio.ambiente_recolecao import AmbienteRecolecao

# --- Imports Políticas e Atuadores ---
from dominio.actuador_mover import ActuadorMover
from dominio.politica_qlearning import PoliticaQlearning
from dominio.politica_fixa import PoliticaFixa           
from dominio.politica_aleatoria import PoliticaAleatoria 

# --- Imports Sensores ---
from dominio.sensor_farol import SensorDireccaoFarol
from dominio.sensor_comum import SensorPosicao, SensorEstadoInterno
from dominio.sensor_recolecao import SensorVisaoRecurso

def limpar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_configuracao():
    limpar_consola()
    print("="*60)
    print("   SIMULADOR DE SISTEMAS MULTI-AGENTE (SMA)")
    print("="*60)
    
    # 1. Escolher Ambiente
    print("\n[1] ESCOLHA O CENÁRIO:")
    print("   1. Farol (Métrica: Passos até o alvo)")
    print("   2. Labirinto (Métrica: Sucesso na saída)")
    print("   3. Recoleção (Métrica: Recursos recolhidos)")
    escolha_amb = input("   >>> Opção (1-3): ")
    
    # 2. Escolher Agente (Política)
    print("\n[2] ESCOLHA A INTELIGÊNCIA:")
    print("   1. Q-Learning (Gera curva de aprendizagem)")
    print("   2. Política Fixa (Baseline)")
    print("   3. Aleatória")
    escolha_pol = input("   >>> Opção (1-3): ")

    # 3. Configurar Mundo
    print("\n[3] CONFIGURAÇÃO DO MUNDO:")
    try:
        largura = int(input("   >>> Largura (default 6): ") or 6)
        altura = int(input("   >>> Altura (default 6): ") or 6)
    except: largura, altura = 6, 6

    # 4. Configurar Treino
    print("\n[4] TREINO:")
    try:
        episodios = int(input("   >>> Nº Episódios Treino (default 200): ") or 200)
    except: episodios = 200

    # 5. Configurar Hiperparâmetros (Só se for Q-Learning)
    # Valores por defeito
    params_rl = {'alpha': 0.1, 'gamma': 0.9, 'epsilon': 0.1}

    if escolha_pol == '1':
        print("\n[5] HIPERPARÂMETROS Q-LEARNING:")
        print("   (Pressione ENTER para usar o valor padrão)")
        try:
            val = input(f"   >>> Learning Rate / Alpha (default 0.1): ")
            if val: params_rl['alpha'] = float(val)

            val = input(f"   >>> Discount Factor / Gamma (default 0.9): ")
            if val: params_rl['gamma'] = float(val)

            val = input(f"   >>> Exploration Rate / Epsilon (default 0.1): ")
            if val: params_rl['epsilon'] = float(val)
        except ValueError:
            print("   ! Valor inválido detetado. A usar defaults...")
    
    return escolha_amb, escolha_pol, largura, altura, episodios, params_rl

def criar_ambiente_e_agente(tipo_amb, tipo_pol, largura, altura, params_rl):
    ambiente = None
    sensores = []
    
    # 1. Setup Ambiente
    if tipo_amb == '1':
        ambiente = AmbienteFarol(largura, altura)
        sensores.append(SensorDireccaoFarol())
    elif tipo_amb == '2':
        ambiente = AmbienteLabirinto(largura, altura)
        sensores.append(SensorPosicao())
        ambiente.posicao_farol = ambiente.saida_pos 
        sensores.append(SensorDireccaoFarol()) 
    elif tipo_amb == '3':
        ambiente = AmbienteRecolecao(largura, altura, num_recursos=5)
        sensores.append(SensorPosicao())
        sensores.append(SensorEstadoInterno())
        sensores.append(SensorVisaoRecurso())
    else: exit()

    # 2. Setup Política
    accoes = ['N', 'S', 'E', 'O']
    politica = None

    if tipo_pol == '1': 
        # Passamos os parâmetros configurados pelo utilizador
        print(f" -> Configurando Q-Learning com: {params_rl}")
        politica = PoliticaQlearning(
            accoes_possiveis=accoes,
            alpha=params_rl['alpha'],
            gamma=params_rl['gamma'],
            epsilon=params_rl['epsilon']
        )
    elif tipo_pol == '2': 
        politica = PoliticaFixa()
    else: 
        politica = PoliticaAleatoria(accoes_possiveis=accoes)

    # 3. Criar Agente
    agente = Agente(id_agente=1, politica=politica)
    for s in sensores: agente.instala(s)
    agente.set_actuador(ActuadorMover())
    
    ambiente.adicionar_agente(agente)
    return ambiente, agente

def main():
    # 1. Menu Completo
    tipo_amb, tipo_pol, w, h, eps, params_rl = menu_configuracao()
    
    # 2. Criação com Parâmetros
    env, agente = criar_ambiente_e_agente(tipo_amb, tipo_pol, w, h, params_rl)
    
    gui = VisualizadorGUI(w, h)
    motor = MotorDeSimulacao(env, visualizador=gui)
    
    logger = Logger("resultados_treino.csv")

    # --- FASE 1: MODO DE APRENDIZAGEM ---
    if tipo_pol == '1': 
        print(f"\n[MODO APRENDIZAGEM] Executando {eps} episódios...")
        agente.politica.modo_treino = True
        start = time.time()
        
        for i in range(1, eps + 1):
            motor.executa_episodio(max_passos=100, visual=False)
            
            # Recolha de Métricas
            sucesso = getattr(env, 'objetivo_alcancado', False)
            if tipo_amb == '3': sucesso = (env.pontuacao_total > 0)
            
            logger.registar_episodio(i, env.passo_atual, agente.recompensa_acumulada, sucesso)
            
            if i % (eps//10) == 0:
                print(f"   Progresso: {i}/{eps} | R: {agente.recompensa_acumulada:.1f}")

        print(f"[MODO APRENDIZAGEM] Concluído em {time.time()-start:.2f}s")
        logger.exportar_csv()

    # --- FASE 2: MODO DE TESTE ---
    input("\n[PRONTO] Pressiona ENTER para iniciar o MODO DE TESTE (Visual)...")
    
    if hasattr(agente.politica, 'modo_treino'):
        agente.politica.modo_treino = False
        agente.politica.epsilon = 0.0

    total_recompensas = 0
    total_sucessos = 0
    num_testes = 5 
    
    print(f"\n[MODO TESTE] Executando {num_testes} episódios de avaliação...")
    
    for i in range(num_testes):
        motor.executa_episodio(max_passos=60, visual=True, delay=0.1)
        
        total_recompensas += agente.recompensa_acumulada
        sucesso_ep = getattr(env, 'objetivo_alcancado', False)
        if tipo_amb == '3' and env.pontuacao_total > 0: sucesso_ep = True
        
        if sucesso_ep: total_sucessos += 1
        print(f"   Episódio {i+1}: {'Sucesso' if sucesso_ep else 'Falha'} (R: {agente.recompensa_acumulada:.1f})")
        time.sleep(0.5)

    print("\n" + "="*40)
    print("   RELATÓRIO DE DESEMPENHO (TESTE)")
    print("="*40)
    print(f"   Configuração: {params_rl if tipo_pol=='1' else 'Política Fixa'}")
    print(f"   Taxa de Sucesso: {(total_sucessos/num_testes)*100}%")
    print(f"   Recompensa Média: {total_recompensas/num_testes:.2f}")
    print("="*40)

    gui.fechar()

if __name__ == "__main__":
    main()