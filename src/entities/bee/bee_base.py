from src.utils.vector import Vector2D

class BeeBase:
    def __init__(self, id, position: Vector2D):
        self.id = id
        self.position = position
        self.energy = 100.0

    def move(self, direction: Vector2D):
        # Upewniamy się, że wektor kierunku jest znormalizowany
        # i pszczoła porusza się o 1 jednostkę na iterację
        magnitude = (direction.x**2 + direction.y**2)**0.5
        if magnitude > 0:
            normalized_direction = Vector2D(
                direction.x / magnitude,
                direction.y / magnitude
            )
            self.position += normalized_direction

    def __repr__(self):
        return f"BeeBase(id={self.id}, position={self.position}, energy={self.energy})"