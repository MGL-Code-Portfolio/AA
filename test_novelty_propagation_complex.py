import unittest
from unittest.mock import MagicMock
from dominio.politica_novelty import PoliticaNovelty
from core.observacao import Observacao

class TestNoveltyPropagationComplex(unittest.TestCase):
    def test_propagation_with_distinct_objects(self):
        # Setup
        # Use observations that look identical but are distinct objects
        obs0 = Observacao({'x': 0, 'y': 0, 'dir_x': 1, 'dir_y': 1})
        obs1_initial = Observacao({'x': 1, 'y': 1, 'dir_x': 1, 'dir_y': 1})

        # When agent moves to step 1, it gets obs1_initial as 'obs_nova'
        # Next step, it gets a NEW object obs1_step2 as 'obs'
        obs1_step2 = Observacao({'x': 1, 'y': 1, 'dir_x': 1, 'dir_y': 1})
        obs2 = Observacao({'x': 2, 'y': 2, 'dir_x': 0, 'dir_y': 0}) # Goal

        actions = ['SE']
        policy = PoliticaNovelty(accoes_possiveis=actions, alpha=0.5, gamma=1.0)
        policy.modo_treino = True

        # Step 1: Agent moves 0 -> 1
        policy.atualizar(obs0, 'SE', -0.1, obs1_initial)

        # Step 2: Agent moves 1 -> 2
        # IMPORTANT: 'obs_antiga' here is obs1_step2, NOT obs1_initial
        policy.atualizar(obs1_step2, 'SE', 20.0, obs2)

        # Finalize
        mock_agent = MagicMock()
        mock_agent.posicao = (2, 2)
        mock_agent.stats = {'visitas_posicao': {(0,0):1, (1,1):1, (2,2):1}}
        policy.finalizar_episodio(mock_agent)

        # Check Q-Values
        q_obs1 = policy._get_q(obs1_initial, 'SE') # Should access same key as obs1_step2
        q_obs0 = policy._get_q(obs0, 'SE')

        print(f"Q(obs1): {q_obs1}")
        print(f"Q(obs0): {q_obs0}")

        self.assertGreater(q_obs1, 0, "Q-value for step T-1 should be positive")
        self.assertGreater(q_obs0, 0, "Q-value for step T-2 should be propagated")

if __name__ == '__main__':
    unittest.main()
