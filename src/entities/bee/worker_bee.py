from src.entities.bee.bee_base import BeeBase
from src.utils.vector import Vector2D
from src.utils.logger_observer import LoggerSubject, FileLogger, ConsoleLogger
import time

class WorkerBee(BeeBase, LoggerSubject):
    def __init__(self, id, position: Vector2D):
        BeeBase.__init__(self, id, position)
        LoggerSubject.__init__(self)
        self.target = None
        self.nectar_capacity = 4  # Adjusted max nectar to simulate ~0.04 mg per flower visit scaled
        self.current_nectar = 0    # Aktualnie niesiony nektar
        self.collection_rate = 1   # Adjusted collection rate to simulate smaller nectar collection per action
        self.target_flower = None   # Kwiat z którego zbiera nektar
        self.steps_without_flower = 0
        self.last_position = None
        self.stuck_count = 0  # licznik prób ruchu bez zmiany pozycji
        self.max_stuck_tries = 5  # maksymalna liczba prób przed zmianą celu
        self.attach(FileLogger('bee', id))
        self.attach(ConsoleLogger('bee'))

    def move(self, direction: Vector2D):
        old_x, old_y = int(self.position.x), int(self.position.y)
        super().move(direction)
        # Zaokrąglamy pozycję do liczb całkowitych
        self.position.x = round(self.position.x)
        self.position.y = round(self.position.y)
        self.notify(f"Pszczoła {self.id} | Pozycja: ({old_x},{old_y}) -> ({int(self.position.x)},{int(self.position.y)}), Nektar: {self.current_nectar}/{self.nectar_capacity}")

    def collect_nectar_from_flower(self, flower):
        """Próbuje zebrać nektar z kwiatu"""
        if self.current_nectar < self.nectar_capacity and flower.nectar > 0:
            space_left = self.nectar_capacity - self.current_nectar
            amount_to_collect = min(self.collection_rate, space_left)
            old_nectar = self.current_nectar
            collected = flower.collect_nectar(amount_to_collect)
            self.current_nectar += collected
            self.notify(f"Pszczoła {self.id} zebrała {collected} nektaru z kwiatu {flower.id}. Stan nektaru: {old_nectar} -> {self.current_nectar}/{self.nectar_capacity}")
            return collected
        return False

    def set_flower_target(self, flower):
        self.target = flower.position
        self.target_flower = flower
        self.steps_without_flower = 0
        self.notify(f"Pszczoła {self.id} - nowy cel: kwiat {flower.id} na pozycji {flower.position}")

    def set_hive_target(self, hive):
        self.target = hive.position
        self.target_flower = None
        self.target_hive = hive
        self.notify(f"Pszczoła {self.id} - nowy cel: ul na pozycji {hive.position}, aktualny nektar: {self.current_nectar}")

    def deposit_nectar_to_hive(self, hive):
        if self.current_nectar > 0:
            old_nectar = self.current_nectar
            hive.store_nectar(self.current_nectar)
            self.notify(f"Oddałam {old_nectar} nektaru do ula. Stan nektaru: {old_nectar} -> 0/{self.nectar_capacity}")
            self.current_nectar = 0

    def update(self):
        if self.target:
            direction = Vector2D(
                self.target.x - self.position.x,
                self.target.y - self.position.y
            )
            length = max(abs(direction.x), abs(direction.y))
            if length > 0:
                direction = Vector2D(
                    round(direction.x / length),
                    round(direction.y / length)
                )
                self.move(direction)
                self.energy -= 0.1

                # Jeśli pszczoła dotarła do celu
                if self.position.distance_to(self.target) < 1:
                    if self.target_flower:
                        # Sprawdź czy kwiat ma jeszcze nektar
                        if self.target_flower.nectar > 0:
                            was_collected = self.collect_nectar_from_flower(self.target_flower)
                        else:
                            self.notify(f"Kwiat nie ma już nektaru, szukam nowego celu")

                        last_flower = self.target_flower  # Zapamiętaj ostatni kwiat
                        # Zawsze zwalniaj cel po próbie zebrania
                        self.target = None
                        self.target_flower = None
                        # Wyczyść referencję do kwiatu (już obsługiwaną przez target_flower = None)

                        # Jeśli mamy pełny nektar, lecimy do ula
                        if self.current_nectar >= self.nectar_capacity:
                            self.notify("Osiągnięto maksymalną pojemność, wracam do ula")
                            self.set_hive_target(self.hive_ref)
                        else:
                            # Zapobiegaj wybraniu tego samego kwiatu
                            self.last_visited_flower = last_flower

                    elif self.target_hive:
                        self.notify("Dotarłam do ula, oddaję nektar")
                        self.deposit_nectar_to_hive(self.target_hive)
                        self.target = None
                        self.target_hive = None
                        self.target_flower = None
                        self.last_visited_flower = None  # Reset ostatnio odwiedzonego kwiatu po oddaniu nektaru

            #time.sleep(0.000005)
