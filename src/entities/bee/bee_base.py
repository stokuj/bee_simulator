from src.utils.vector import Vector2D

class BeeBase:
    def __init__(self, id, position: Vector2D):
        self.id = id
        self.position = position
        self.energy = 100.0

    def move(self, direction: Vector2D):
        self.position += direction

    def __repr__(self):
        return f"BeeBase(id={self.id}, position={self.position}, energy={self.energy})"