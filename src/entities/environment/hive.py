from src.utils.logger_observer import LoggerSubject, FileLogger, ConsoleLogger

class Hive(LoggerSubject):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.nectar_stored = 0
        self.max_nectar_capacity = 1000
        self.attach(FileLogger('environment/hive', 'hive'))
        self.attach(ConsoleLogger('hive'))

    def store_nectar(self, amount):
        old_amount = self.nectar_stored
        self.nectar_stored += amount
        self.notify(f"Zmiana nektaru w ulu: {old_amount} -> {self.nectar_stored} (dodano {amount})")
        return True

    def get_stored_nectar(self):
        return self.nectar_stored

    def __repr__(self):
        return f"Hive(position={self.position}, stored_nectar={self.nectar_stored})"
