from ..entities.environment.hive import Hive
from ..entities.environment.flower import Flower
from collections import namedtuple

Position = namedtuple("Position", ["x", "y"])

class MapGenerator:
    def generate_basic_map(self):
        # Tworzy prostą mapę z jednym ulem i kilkoma kwiatkami
        hive = Hive(Position(5, 5))
        flowers = [
            Flower(Position(2, 3)),
            Flower(Position(7, 8)),
            Flower(Position(4, 6)),
        ]
        return [hive] + flowers