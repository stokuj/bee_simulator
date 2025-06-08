import unittest
from src.entities.bee.worker_bee import WorkerBee
from src.utils.vector import Vector2D

class TestWorkerBeeBehavior(unittest.TestCase):
    def setUp(self):
        self.bee = WorkerBee(id="bee1", position=Vector2D(0, 0))

    def test_creation(self):
        self.assertEqual(self.bee.id, "bee1")
        self.assertEqual(self.bee.position.x, 0)
        self.assertEqual(self.bee.position.y, 0)

    def test_movement(self):
        initial_position = self.bee.position
        self.bee.move(Vector2D(1, 1))
        self.assertNotEqual(self.bee.position, initial_position)
        self.assertEqual(self.bee.position.x, 1)
        self.assertEqual(self.bee.position.y, 1)

    def test_react_to_pheromone(self):
        # Prosty test reakcji na feromon (symulacja)
        pheromone_position = Vector2D(5, 5)
        self.bee.react_to_pheromone(pheromone_position)
        # Sprawdź, czy pszczoła zmieniła kierunek w stronę feromonu
        self.assertTrue(self.bee.is_moving_towards(pheromone_position))

if __name__ == "__main__":
    unittest.main()