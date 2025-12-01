import time
import os

# --- Imports do Core e Simulação ---
from core.agente import Agente
from simulacao.motor import MotorDeSimulacao
from simulacao.visualizador_gui import VisualizadorGUI

# --- Imports do Domínio (Ambientes) ---
from dominio.ambiente_farol import AmbienteFarol
from dominio.ambiente_labirinto import AmbienteLabirinto
from dominio.ambiente_recolecao import AmbienteRecolecao

# --- Imports do Domínio (Agentes/Sensores) ---
from dominio.politica_qlearning import PoliticaQlearning
from dominio.actuador_mover import ActuadorMover
from dominio.sensor_farol import SensorDireccaoFarol
from dominio.sensor_comum import SensorPosicao, SensorEstadoInterno

def limpar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_configuracao():
    limpar_consola()
    print("="*40)
    print("   CONFIGURADOR DE SIMULAÇÃO SMA")
    print("="*40)
    
    # 1. Escolher Ambiente
    print("\n[1] Escolha o Cenário:")
    print("   1. Problema do Farol (Navegação Simples)")
    print("   2. Labirinto (Obstáculos)")
    print("   3. Recoleção / Foraging (Recursos e Ninho)")
    
    escolha_amb = input("   >>> Opção (1-3): ")
    
    # 2. Configurar Tamanho
    print("\n[2] Configuração do Mundo:")
    try:
        largura = int(input("   >>> Largura da Grelha (padrao 6): ") or 6)
        altura = int(input("   >>> Altura da Grelha (padrao 6): ") or 6)
    except ValueError:
        largura, altura = 6, 6
        print("   ! Valor inválido. Usando 6x6.")

    # 3. Configurar Treino
    print("\n[3] Configuração de Aprendizagem:")
    try:
        episodios = int(input("   >>> Nº Episódios de Treino (padrao 200): ") or 200)
    except ValueError:
        episodios = 200
    
    return escolha_amb, largura, altura, episodios

def criar_ambiente_e_agente(escolha, largura, altura):
    ambiente = None
    sensores = []
    
    # Setup Específico por Cenário
    if escolha == '1': # Farol
        print(f" -> Criando Ambiente Farol ({largura}x{altura})...")
        ambiente = AmbienteFarol(largura, altura)
        sensores.append(SensorDireccaoFarol()) # Sensor específico
        
    elif escolha == '2': # Labirinto
        print(f" -> Criando Labirinto ({largura}x{altura})...")
        ambiente = AmbienteLabirinto(largura, altura)
        sensores.append(SensorPosicao()) # Precisa saber onde está para desviar paredes

    elif escolha == '3': # Recoleção
        print(f" -> Criando Ambiente Recoleção ({largura}x{altura})...")
        ambiente = AmbienteRecolecao(largura, altura, num_recursos=4)
        sensores.append(SensorPosicao())       # Saber onde está
        sensores.append(SensorEstadoInterno()) # Saber se carrega algo
        
    else:
        print("Opção inválida! A sair...")
        exit()

    # Configuração Comum do Agente
    print(" -> Configurando Agente Q-Learning...")
    politica = PoliticaQlearning(accoes_possiveis=['N', 'S', 'E', 'O'])
    agente = Agente(id_agente=1, politica=politica)
    
    # Instalar Sensores Selecionados
    for s in sensores:
        agente.instala(s)
    
    # Instalar Atuador
    agente.set_actuador(ActuadorMover())
    
    ambiente.adicionar_agente(agente)
    return ambiente, agente

def main():
    # 1. Executar Menu
    opcao, largura, altura, n_episodios = menu_configuracao()
    
    # 2. Instanciar Classes
    env, agente = criar_ambiente_e_agente(opcao, largura, altura)
    
    # 3. Setup Motor e GUI
    gui = VisualizadorGUI(largura, altura)
    motor = MotorDeSimulacao(env, visualizador=gui)

    # 4. Modo Treino (Rápido)
    print(f"\n[TREINO] Iniciando {n_episodios} episódios...")
    agente.politica.modo_treino = True
    start = time.time()
    
    # Barra de progresso simples
    for i in range(1, n_episodios + 1):
        motor.executa_episodio(max_passos=100, visual=False)
        if i % (n_episodios // 10) == 0:
            print(f"   Progresso: {i}/{n_episodios} eps | Recompensa (último): {agente.recompensa_acumulada:.2f}")

    tempo_treino = time.time() - start
    print(f"[TREINO] Concluído em {tempo_treino:.2f}s.")

    # 5. Modo Teste (Visual)
    input("\n[PRONTO] Pressiona ENTER para abrir a janela de visualização...")
    
    print("[TESTE] A executar simulação gráfica...")
    agente.politica.modo_treino = False
    agente.politica.epsilon = 0.0 # Sem movimentos aleatórios
    
    # Loop para permitir repetir o teste visual
    while True:
        motor.executa_episodio(max_passos=50, visual=True, delay=0.2)
        
        status = "OBJETIVO ALCANCADO" if getattr(env, 'objetivo_alcancado', False) else "TERMINADO"
        print(f"   Resultado: {status} | Recompensa: {agente.recompensa_acumulada}")
        
        rep = input("Repetir visualização? (s/n): ").lower()
        if rep != 's':
            break

    print("Encerrando...")
    gui.fechar()

if __name__ == "__main__":
    main()