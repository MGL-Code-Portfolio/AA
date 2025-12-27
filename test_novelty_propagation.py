import unittest
from unittest.mock import MagicMock
from dominio.politica_novelty import PoliticaNovelty
from core.observacao import Observacao

class TestNoveltyPropagation(unittest.TestCase):
    def test_backward_propagation(self):
        # Setup
        # Use a simple "grid" observation mock
        # State 0 -> State 1 -> State 2 (Goal)
        # Goal reward = 10 (external) + Novelty

        # We need to simulate the key generation logic of PoliticaQlearning
        # key = tuple(sorted(obs.dados.items()))

        obs0 = Observacao({'x': 0})
        obs1 = Observacao({'x': 1})
        obs2 = Observacao({'x': 2}) # Goal

        # Initialize Policy
        # Use simple actions
        actions = ['R']
        policy = PoliticaNovelty(accoes_possiveis=actions, alpha=0.5, gamma=1.0)
        policy.modo_treino = True

        # Step 1: Agent moves 0 -> 1
        policy.atualizar(obs0, 'R', -1, obs1)

        # Step 2: Agent moves 1 -> 2
        policy.atualizar(obs1, 'R', 10, obs2) # High external reward

        # Manually finalize episode (normally called by Motor)
        # Mocking Agent for Novelty Calculation (centroid)
        mock_agent = MagicMock()
        mock_agent.posicao = (2, 0)

        policy.finalizar_episodio(mock_agent)

        # Check Q-Values
        # Expected propagation:
        # Step 2 (Last): R_final = Intrinsica + External_Sum = (~1.0) + (-1 + 10) = ~10.0
        # obs1 -> 'R' should get Q = alpha * (R_final + gamma*maxQ(obs2))
        # maxQ(obs2) is 0 initially.
        # Q(obs1, 'R') = 0.5 * (10.0 + 0 - 0) = 5.0

        # Step 1 (Second to last): R = 0
        # obs0 -> 'R' should get Q = alpha * (0 + gamma*Q(obs1))
        # Q(obs1, 'R') is 5.0.
        # Q(obs0, 'R') = 0.5 * (0 + 1.0 * 5.0 - 0) = 2.5

        q_obs1 = policy._get_q(obs1, 'R')
        q_obs0 = policy._get_q(obs0, 'R')

        print(f"Q(obs1): {q_obs1}")
        print(f"Q(obs0): {q_obs0}")

        self.assertGreater(q_obs1, 0, "Q-value for step T-1 should be positive")
        self.assertGreater(q_obs0, 0, "Q-value for step T-2 should be propagated and positive")

if __name__ == '__main__':
    unittest.main()
