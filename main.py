import time
from core.agente import Agente
from dominio.ambiente_farol import AmbienteFarol
from dominio.politica_qlearning import PoliticaQlearning
from dominio.sensor_farol import SensorDireccaoFarol
from dominio.actuador_mover import ActuadorMover
from simulacao.motor import MotorDeSimulacao

def main():
    print(">>> Inicializando Sistema Multi-Agente Modular")
    
    # 1. Setup do Ambiente
    env = AmbienteFarol(largura=6, altura=6)
    
    # 2. Setup do Agente
    politica = PoliticaQlearning(accoes_possiveis=['N', 'S', 'E', 'O'])
    agente = Agente(id_agente=1, politica=politica)
    agente.instala(SensorDireccaoFarol())
    agente.set_actuador(ActuadorMover())
    
    env.adicionar_agente(agente)
    
    # 3. Setup do Motor
    motor = MotorDeSimulacao(env)

    # 4. Fase de Treino (Learning Mode)
    print("\n[TREINO] A executar 200 episódios de Q-Learning...")
    agente.politica.modo_treino = True
    start = time.time()
    
    for i in range(200):
        motor.executa_episodio(max_passos=50, visual=False)
    
    print(f"[TREINO] Concluído em {time.time() - start:.2f}s")
    
    # 5. Fase de Teste (Exploitation Mode)
    print("\n[TESTE] A mostrar o resultado final...")
    agente.politica.modo_treino = False # Desliga exploração aleatória
    agente.politica.epsilon = 0.0
    
    input("Pressiona ENTER para ver a simulação...")
    motor.executa_episodio(max_passos=30, visual=True, delay=0.3)
    
    if env.objetivo_alcancado:
        print("\nSUCESSO: O agente chegou ao Farol!")
    else:
        print("\nFALHA: O agente perdeu-se.")

if __name__ == "__main__":
    main()