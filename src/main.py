import time
import pygame
import random
import math
from src.environment.map_generator import MapGenerator
from src.entities.bee.worker_bee import WorkerBee
from src.utils.vector import Vector2D
from src.utils.config import ConfigManager

def draw_environment(screen, environment_objects):
    screen.fill((255, 255, 255))  # białe tło
    for obj in environment_objects:
        if obj.__class__.__name__ == "Hive":
            pygame.draw.rect(screen, (255, 215, 0), pygame.Rect(obj.position.x * 6, obj.position.y * 6, 6, 6))  # złoty kwadrat
        elif obj.__class__.__name__ == "Flower":
            color = (255, 0, 0) if obj.nectar > 0 else (0, 0, 0)
            pygame.draw.circle(screen, color, (int(obj.position.x * 6 + 3), int(obj.position.y * 6 + 3)), 2)

def draw_bees(screen, bees):
    for bee in bees:
        pygame.draw.circle(screen, (0, 0, 255), (int(bee.position.x * 6 + 3), int(bee.position.y * 6 + 3)), 2)  # niebieskie kółko

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 1200))  # Zmniejszony rozmiar okna do 1200x1200
    pygame.display.set_caption("Bee Simulator")

    # Załaduj konfigurację
    config = ConfigManager("config/simulation_config.ini")
    config.load()

    # Wygeneruj mapę
    map_gen = MapGenerator()
    environment_objects = map_gen.generate_basic_map()
    hive = [obj for obj in environment_objects if obj.__class__.__name__ == "Hive"][0]

    # Utwórz 25 pszczół (5x więcej) wokół ula (pozycja 100,100)
    bees = []
    for i in range(25):
        # Losowe pozycje w promieniu 20 jednostek od ula
        angle = random.uniform(0, 2 * 3.14159)
        radius = random.uniform(5, 20)
        x = 100 + radius * math.cos(angle)
        y = 100 + radius * math.sin(angle)
        bees.append(WorkerBee(id=f"bee{i+1}", position=Vector2D(x, y)))
    for bee in bees:
        bee.hive_ref = hive
        # Początkowe ustawienie celu dla każdej pszczoły
        flowers = [obj for obj in environment_objects if obj.__class__.__name__ == "Flower" and obj.nectar > 0]
        if flowers:
            flower = random.choice(flowers)
            bee.set_flower_target(flower)

    clock = pygame.time.Clock()
    running = True

    # Słownik do przechowywania ostatnich pozycji pszczół i liczników bezruchu
    bees_last_positions = {bee.id: {"position": bee.position, "static_count": 0} for bee in bees}
    max_static_count = 50  # Po tylu iteracjach bez ruchu uznajemy, że program się zawiesił

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Sprawdź czy są jeszcze kwiaty z nektarem
        available_flowers = [obj for obj in environment_objects if obj.__class__.__name__ == "Flower" and obj.nectar > 0]
        if not available_flowers:
            print("Brak kwiatów z nektarem! Koniec symulacji.")
            running = False
            continue

        # Licznik pszczół, które się nie ruszają
        total_static_bees = 0

        # Aktualizacja pszczół
        for bee in bees:
            # Sprawdzenie czy pszczoła się porusza
            current_pos = (bee.position.x, bee.position.y)
            last_pos = (bees_last_positions[bee.id]["position"].x, bees_last_positions[bee.id]["position"].y)

            if current_pos == last_pos:
                bees_last_positions[bee.id]["static_count"] += 1
                if bees_last_positions[bee.id]["static_count"] >= max_static_count:
                    total_static_bees += 1
            else:
                bees_last_positions[bee.id]["static_count"] = 0

            # Aktualizacja ostatniej pozycji
            bees_last_positions[bee.id]["position"] = Vector2D(bee.position.x, bee.position.y)

            # Standardowa logika przydzielania celów
            needs_new_target = (
                not bee.target and
                not getattr(bee, 'target_hive', None) and
                bee.current_nectar < bee.nectar_capacity
            )

            if bee.current_nectar >= bee.nectar_capacity and not getattr(bee, 'target_hive', None):
                bee.set_hive_target(hive)
            elif needs_new_target:
                # Wybierz nowy kwiat, ale nie ten sam co ostatnio
                valid_flowers = [f for f in available_flowers if f != getattr(bee, 'last_visited_flower', None)]
                if valid_flowers:
                    flower = random.choice(valid_flowers)
                    bee.set_flower_target(flower)

            bee.update()

        # Sprawdzenie czy wszystkie pszczoły stoją
        if total_static_bees == len(bees):
            print(f"UWAGA: Program może być zawieszony - wszystkie pszczoły stoją w miejscu przez {max_static_count} iteracji!")
            # Opcjonalnie: możemy wymusić zakończenie programu
            # running = False
            # continue

        # Usuwanie kwiatów bez nektaru
        environment_objects = [obj for obj in environment_objects if not (obj.__class__.__name__ == "Flower" and obj.nectar <= 0)]

        # Rysowanie
        draw_environment(screen, environment_objects)
        draw_bees(screen, bees)

        pygame.display.flip()
        clock.tick(170)  # 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()