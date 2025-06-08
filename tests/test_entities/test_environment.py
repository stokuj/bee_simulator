import unittest
from src.entities.environment.hive import Hive
from src.entities.environment.flower import Flower
from src.environment.map_generator import MapGenerator

class TestEnvironment(unittest.TestCase):
    def setUp(self):
        # Przygotowanie mapy z ulem i kwiatkami
        self.map_generator = MapGenerator()
        self.map_data = self.map_generator.generate_basic_map()

    def test_hive_presence(self):
        # Sprawdź, czy na mapie jest ul
        hive_positions = [obj.position for obj in self.map_data if isinstance(obj, Hive)]
        self.assertTrue(len(hive_positions) > 0, "Mapa powinna zawierać ul")

    def test_flower_presence(self):
        # Sprawdź, czy na mapie są kwiatki
        flower_positions = [obj.position for obj in self.map_data if isinstance(obj, Flower)]
        self.assertTrue(len(flower_positions) > 0, "Mapa powinna zawierać kwiatki")

if __name__ == "__main__":
    unittest.main()