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


    def test_set_flower_target(self):
        class MockFlower:
            def __init__(self, position, nectar=100):
                self.position = position
                self.nectar = nectar
                self.id = "mock_flower"

            def collect_nectar(self, amount):
                collected = min(amount, self.nectar)
                self.nectar -= collected
                return collected

        flower = MockFlower(Vector2D(10, 10))
        self.bee.set_flower_target(flower)
        self.assertEqual(self.bee.target, flower.position)
        self.assertEqual(self.bee.target_flower, flower)
        self.assertEqual(self.bee.target_flower, flower)

    def test_collect_nectar_from_flower(self):
        class MockFlower:
            def __init__(self, position, nectar=100):
                self.position = position
                self.nectar = nectar
                self.id = "mock_flower"

            def collect_nectar(self, amount):
                collected = min(amount, self.nectar)
                self.nectar -= collected
                return collected

        flower = MockFlower(Vector2D(10, 10), nectar=5)
        self.bee.nectar_capacity = 10
        self.bee.collection_rate = 2
        
        # Collect some nectar
        collected_amount = self.bee.collect_nectar_from_flower(flower)
        self.assertEqual(collected_amount, 2)
        self.assertEqual(self.bee.current_nectar, 2)
        self.assertEqual(flower.nectar, 3)

        # Collect remaining nectar
        collected_amount = self.bee.collect_nectar_from_flower(flower)
        self.assertEqual(collected_amount, 2) # Should collect another 2
        self.assertEqual(self.bee.current_nectar, 4)
        self.assertEqual(flower.nectar, 1)

        # Collect last nectar
        collected_amount = self.bee.collect_nectar_from_flower(flower)
        self.assertEqual(collected_amount, 1) # Should collect remaining 1
        self.assertEqual(self.bee.current_nectar, 5)
        self.assertEqual(flower.nectar, 0)
        
        # Try to collect from empty flower
        collected_amount = self.bee.collect_nectar_from_flower(flower)
        self.assertEqual(collected_amount, 0)
        self.assertEqual(self.bee.current_nectar, 5)


    def test_set_hive_target(self):
        class MockHive:
            def __init__(self, position):
                self.position = position
        hive = MockHive(Vector2D(0, 0))
        self.bee.set_hive_target(hive)
        self.assertEqual(self.bee.target, hive.position)
        self.assertEqual(self.bee.target_hive, hive)
        self.assertIsNone(self.bee.target_flower)

    def test_deposit_nectar_to_hive(self):
        class MockHive:
            def __init__(self, position):
                self.position = position
                self.nectar_stored = 0
            def store_nectar(self, amount):
                self.nectar_stored += amount
        hive = MockHive(Vector2D(0, 0))
        self.bee.current_nectar = 5
        self.bee.deposit_nectar_to_hive(hive)
        self.assertEqual(hive.nectar_stored, 5)
        self.assertEqual(self.bee.current_nectar, 0)

if __name__ == "__main__":
    unittest.main()