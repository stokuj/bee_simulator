import unittest
from src.utils.config import ConfigManager

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.config = ConfigManager("config/simulation_config.ini")

    def test_load_config(self):
        self.config.load()
        self.assertIsNotNone(self.config.get("simulation", "speed"))

    def test_set_and_save_config(self):
        self.config.set("simulation", "speed", "2.0")
        self.config.save()
        self.config.load()
        self.assertEqual(self.config.get("simulation", "speed"), "2.0")

if __name__ == "__main__":
    unittest.main()