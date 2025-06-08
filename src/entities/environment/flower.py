class Flower:
    def __init__(self, position, nectar_amount=100):
        self.position = position
        self.nectar_amount = nectar_amount

    def __repr__(self):
        return f"Flower(position={self.position}, nectar_amount={self.nectar_amount})"