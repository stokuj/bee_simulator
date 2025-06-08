from src.utils.logger_observer import LoggerSubject, FileLogger, ConsoleLogger


class Flower(LoggerSubject):
    flower_count = 0

    def __init__(self, position, initial_nectar=100):
        super().__init__()
        Flower.flower_count += 1
        self.id = f"flower_{Flower.flower_count}"
        self.position = position
        self.nectar = initial_nectar
        self.max_nectar = initial_nectar
        self.attach(FileLogger('environment/flowers', self.id))
        self.attach(ConsoleLogger('flower'))
        self.notify(f"Utworzono kwiat z {initial_nectar} nektaru")

    def collect_nectar(self, amount):
        """Zbiera nektar z kwiatu. Zwraca faktyczną ilość zebranego nektaru"""
        old_amount = self.nectar
        if self.nectar >= amount:
            self.nectar -= amount
            collected = amount
        else:
            collected = self.nectar
            self.nectar = 0

        self.notify(f"Zmiana nektaru w kwiecie: {old_amount} -> {self.nectar} (zebrano {collected})")
        return collected

    def regenerate_nectar(self):
        """Regeneruje małą ilość nektaru"""
        if self.nectar < self.max_nectar:
            self.nectar = min(self.max_nectar, self.nectar + 1)

    def __repr__(self):
        return f"Flower(position={self.position}, nectar_amount={self.nectar})"
