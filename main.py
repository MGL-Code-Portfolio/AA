import time
import os

# --- Imports Core ---
from core.agente import Agente
from simulacao.motor import MotorDeSimulacao
from simulacao.visualizador_gui import VisualizadorGUI
from simulacao.logger import Logger  # <--- NOVO IMPORT

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
    
    print("\n[1] ESCOLHA O CENÁRIO:")
    print("   1. Farol (Métrica: Passos até o alvo)")
    print("   2. Labirinto (Métrica: Sucesso na saída)")
    print("   3. Recoleção (Métrica: Recursos recolhidos)")
    escolha_amb = input("   >>> Opção (1-3): ")
    
    print("\n[2] ESCOLHA A INTELIGÊNCIA:")
    print("   1. Q-Learning (Gera curva de aprendizagem)")
    print("   2. Política Fixa (Baseline)")
    print("   3. Aleatória")
    escolha_pol = input("   >>> Opção (1-3): ")

    try:
        largura = int(input("\n   >>> Largura (default 6): ") or 6)
        altura = int(input("   >>> Altura (default 6): ") or 6)
        episodios = int(input("   >>> Nº Episódios Treino (default 200): ") or 200)
    except:
        largura, altura, episodios = 6, 6, 200
    
    return escolha_amb, escolha_pol, largura, altura, episodios

def criar_ambiente_e_agente(tipo_amb, tipo_pol, largura, altura):
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
    if tipo_pol == '1': politica = PoliticaQlearning(accoes_possiveis=accoes)
    elif tipo_pol == '2': politica = PoliticaFixa()
    else: politica = PoliticaAleatoria(accoes_possiveis=accoes)

    # 3. Criar Agente
    agente = Agente(id_agente=1, politica=politica)
    for s in sensores: agente.instala(s)
    agente.set_actuador(ActuadorMover())
    
    ambiente.adicionar_agente(agente)
    return ambiente, agente

def main():
    tipo_amb, tipo_pol, w, h, eps = menu_configuracao()
    env, agente = criar_ambiente_e_agente(tipo_amb, tipo_pol, w, h)
    gui = VisualizadorGUI(w, h)
    motor = MotorDeSimulacao(env, visualizador=gui)
    
    # Logger para cumprir requisito de "registar dados de desempenho"
    logger = Logger("resultados_treino.csv")

    # --- FASE 1: MODO DE APRENDIZAGEM ---
    # "A politica pode ser modificada... registar dados" [Enunciado: C.1]
    
    if tipo_pol == '1': # Só treina se for Q-Learning
        print(f"\n[MODO APRENDIZAGEM] Executando {eps} episódios...")
        agente.politica.modo_treino = True
        start = time.time()
        
        for i in range(1, eps + 1):
            motor.executa_episodio(max_passos=100, visual=False)
            
            # Recolha de Métricas para o Relatório
            sucesso = getattr(env, 'objetivo_alcancado', False)
            if tipo_amb == '3': # Recoleção: Sucesso é apanhar recursos
                sucesso = (env.pontuacao_total > 0)
            
            # Regista no CSV
            logger.registar_episodio(
                episodio=i, 
                passos=env.passo_atual, 
                recompensa=agente.recompensa_acumulada,
                sucesso=sucesso
            )
            
            if i % (eps//10) == 0:
                print(f"   Progresso: {i}/{eps} | R: {agente.recompensa_acumulada:.1f}")

        print(f"[MODO APRENDIZAGEM] Concluído em {time.time()-start:.2f}s")
        logger.exportar_csv() # Gera o ficheiro para o Excel

    # --- FASE 2: MODO DE TESTE ---
    # "Política fixa/pré-treinada... foco na avaliação do desempenho" [Enunciado: C.2]
    
    input("\n[PRONTO] Pressiona ENTER para iniciar o MODO DE TESTE (Visual)...")
    
    # Congelar a aprendizagem (Requisito obrigatório)
    if hasattr(agente.politica, 'modo_treino'):
        agente.politica.modo_treino = False
        agente.politica.epsilon = 0.0

    total_recompensas = 0
    total_sucessos = 0
    num_testes = 5 # Fazemos 5 testes para tirar média
    
    print(f"\n[MODO TESTE] Executando {num_testes} episódios de avaliação...")
    
    for i in range(num_testes):
        print(f"   Teste {i+1} a rodar...")
        motor.executa_episodio(max_passos=60, visual=True, delay=0.1)
        
        # Calcular Métricas Finais
        total_recompensas += agente.recompensa_acumulada
        sucesso_ep = getattr(env, 'objetivo_alcancado', False)
        if tipo_amb == '3' and env.pontuacao_total > 0: sucesso_ep = True
        
        if sucesso_ep: total_sucessos += 1
        
        # Pausa curta entre testes visuais
        time.sleep(0.5)

    # Apresentar Relatório Final na Consola
    print("\n" + "="*40)
    print("   RELATÓRIO DE DESEMPENHO (TESTE)")
    print("="*40)
    print(f"   Taxa de Sucesso: {(total_sucessos/num_testes)*100}%")
    print(f"   Recompensa Média: {total_recompensas/num_testes:.2f}")
    print("="*40)

    gui.fechar()

if __name__ == "__main__":
    main()