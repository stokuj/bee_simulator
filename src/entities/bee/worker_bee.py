from src.entities.bee.bee_base import BeeBase
from src.utils.vector import Vector2D

class WorkerBee(BeeBase):
    def __init__(self, id, position: Vector2D):
        super().__init__(id, position)
        self.target = None

    def move(self, direction: Vector2D):
        super().move(direction)

    def react_to_pheromone(self, pheromone_position: Vector2D):
        # Prosta reakcja: ustaw cel na pozycję feromonu
        self.target = pheromone_position

    def is_moving_towards(self, position: Vector2D):
        if self.target is None:
            return False
        # Sprawdź, czy cel jest blisko pozycji
        distance = self.position.distance_to(position)
        target_distance = self.position.distance_to(self.target)
        return distance <= target_distance

    def update(self):
        # Prosta logika ruchu w kierunku celu
        if self.target:
            direction = Vector2D(
                self.target.x - self.position.x,
                self.target.y - self.position.y
            )
            # Normalizacja kierunku do jednostkowego wektora
            length = (direction.x**2 + direction.y**2)**0.5
            if length > 0:
                direction = Vector2D(direction.x / length, direction.y / length)
                self.move(direction)
                # Zmniejsz energię przy ruchu
                self.energy -= 0.1
                # Jeśli pszczoła dotarła do celu, usuń cel
                if self.position.distance_to(self.target) < 0.1:
                    self.target = None