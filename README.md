# Simulador de Sistemas Multi-Agente (SMA)

Este projeto implementa um simulador para ambientes multi-agente, onde agentes aprendem a navegar e interagir com diferentes cenários utilizando Aprendizagem por Reforço (Q-Learning), além de políticas fixas e aleatórias.

## Funcionalidades Principais

*   **Ambientes Diversos**:
    *   **Farol**: Agentes devem encontrar um farol (alvo fixo) com base em sensores de direção.
    *   **Labirinto**: Agentes navegam em um labirinto para encontrar a saída.
    *   **Recoleção**: Agentes recolhem recursos espalhados pelo mapa, gerenciando energia/capacidade.
*   **Políticas de Controle**:
    *   **Q-Learning**: Aprendizagem tabular baseada em recompensas.
    *   **Fixa**: Comportamento pré-programado simples.
    *   **Aleatória**: Movimentação randômica (baseline).
*   **Visualização**:
    *   Interface gráfica em tempo real (PyGame) mostrando os agentes e o ambiente.
    *   Gráficos de análise de desempenho (Matplotlib).

## Instalação

Certifique-se de ter o Python instalado. Recomenda-se o uso de um ambiente virtual.

1.  Instale as dependências listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

As principais dependências são:
*   `pygame`: Para a interface gráfica.
*   `pandas`: Para manipulação de dados e logs.
*   `matplotlib`: Para geração de gráficos e heatmaps.

## Como Usar

Para iniciar o simulador, execute o ficheiro principal:

```bash
python main.py
```

O programa apresentará um menu interativo no terminal. Siga as instruções para configurar a simulação:

1.  **Escolha o Cenário**: Selecione entre Farol, Labirinto ou Recoleção.
2.  **Escolha a Inteligência**: Selecione o algoritmo de controle (Q-Learning, Fixa, Aleatória).
3.  **Parâmetros do Mundo**: Defina a largura e altura da grelha (ex: 10x10) e o número de agentes.
4.  **Modo de Execução**:
    *   **Treino Completo + Teste Visual**: Executa N episódios de treino (sem visualização lenta) e depois mostra o resultado final visualmente.
    *   **Apenas Treino**: Executa o treino e gera os ficheiros de dados e Q-Table, sem abrir a janela visual.
    *   **Apenas Teste Visual**: Carrega uma Q-Table existente (se houver) e mostra o comportamento dos agentes.

## Visualizações Geradas

Após a execução (especialmente no modo de treino), o sistema gera ficheiros na raiz do projeto:

*   **Curva de Aprendizagem (`*_curva_aprendizagem.png`)**: Gráfico mostrando a evolução da recompensa média por episódio. Útil para verificar se o agente está a aprender (a curva deve subir e estabilizar).
*   **Heatmap de Valores Q (`*_heatmap.png`)**: Mapa de calor que mostra o "valor" de cada célula da grelha. Cores mais quentes indicam estados onde o agente espera receber maior recompensa futura.
*   **Mapa de Política (`*_politica.png`)**: Visualização com setas indicando a direção preferencial (melhor ação aprendida) em cada célula da grelha. Ajuda a entender a estratégia de navegação do agente.
*   **Logs CSV (`*_simulacao.csv`)**: Dados brutos de cada episódio (passos, recompensas, sucesso) para análise detalhada.
*   **Q-Tables (`qtable_*.pkl`)**: Ficheiros de persistência do aprendizado do agente.

## Estrutura do Projeto

*   `core/`: Classes base (Agente, Ambiente, Política, Sensor).
*   `dominio/`: Implementações específicas dos ambientes e políticas.
*   `simulacao/`: Motor de simulação, logger e visualizadores.
*   `main.py`: Ponto de entrada da aplicação.
