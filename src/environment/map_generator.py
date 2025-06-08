from ..entities.environment.hive import Hive
from ..entities.environment.flower import Flower
from collections import namedtuple
import random

Position = namedtuple("Position", ["x", "y"])

class MapGenerator:
    def generate_basic_map(self):
        # Tworzy większą mapę z jednym ulem i większą ilością kwiatów
        hive = Hive(Position(10, 10))  # Ul na środku mapy

        # Generowanie 14 kwiatów z różnymi ilościami nektaru
        flowers = [
            Flower(Position(2, 3), initial_nectar=random.randint(4, 10)),
            Flower(Position(15, 8), initial_nectar=random.randint(4, 10)),
            Flower(Position(4, 16), initial_nectar=random.randint(4, 10)),
            Flower(Position(18, 18), initial_nectar=random.randint(4, 10)),
            Flower(Position(7, 12), initial_nectar=random.randint(4, 10)),
            Flower(Position(13, 5), initial_nectar=random.randint(4, 10)),
            Flower(Position(9, 15), initial_nectar=random.randint(4, 10)),
            Flower(Position(3, 8), initial_nectar=random.randint(4, 10)),
            Flower(Position(16, 12), initial_nectar=random.randint(4, 10)),
            Flower(Position(6, 18), initial_nectar=random.randint(4, 10)),
            Flower(Position(14, 15), initial_nectar=random.randint(4, 10)),
            Flower(Position(8, 7), initial_nectar=random.randint(4, 10)),
            Flower(Position(17, 4), initial_nectar=random.randint(4, 10)),
            Flower(Position(12, 9), initial_nectar=random.randint(4, 10))
        ]
        return [hive] + flowers