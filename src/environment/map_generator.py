from ..entities.environment.hive import Hive
from ..entities.environment.flower import Flower
from collections import namedtuple
import random

Position = namedtuple("Position", ["x", "y"])

class MapGenerator:
    def generate_basic_map(self):
        # Tworzy 10x większą mapę z jednym ulem i 5x większą ilością kwiatów
        hive = Hive(Position(100, 100))  # Ul na środku mapy (200x200)

        # Generowanie 70 kwiatów (5x więcej) z losowymi pozycjami na większej mapie
        flowers = []
        for _ in range(70):
            x = random.randint(10, 190)  # Unikamy skrajnych krawędzi
            y = random.randint(10, 190)
            flowers.append(Flower(Position(x, y), initial_nectar=random.randint(4, 10)))
        return [hive] + flowers