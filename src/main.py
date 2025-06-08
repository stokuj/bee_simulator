import time
import pygame
import random
from src.environment.map_generator import MapGenerator
from src.entities.bee.worker_bee import WorkerBee
from src.utils.vector import Vector2D
from src.utils.config import ConfigManager

def draw_environment(screen, environment_objects):
    screen.fill((255, 255, 255))  # białe tło
    for obj in environment_objects:
        if obj.__class__.__name__ == "Hive":
            pygame.draw.rect(screen, (255, 215, 0), pygame.Rect(obj.position.x * 40, obj.position.y * 40, 40, 40))  # złoty kwadrat
        elif obj.__class__.__name__ == "Flower":
            pygame.draw.circle(screen, (255, 0, 0), (int(obj.position.x * 40 + 20), int(obj.position.y * 40 + 20)), 15)  # czerwone kółko

def draw_bees(screen, bees):
    for bee in bees:
        pygame.draw.circle(screen, (0, 0, 255), (int(bee.position.x * 40 + 20), int(bee.position.y * 40 + 20)), 10)  # niebieskie kółko

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Bee Simulator")

    # Załaduj konfigurację
    config = ConfigManager("config/simulation_config.ini")
    config.load()

    # Wygeneruj mapę
    map_gen = MapGenerator()
    environment_objects = map_gen.generate_basic_map()

    # Utwórz pszczoły robotnice
    bees = [
        WorkerBee(id="bee1", position=Vector2D(5, 5)),
        WorkerBee(id="bee2", position=Vector2D(6, 5)),
    ]

    clock = pygame.time.Clock()
    running = True
    last_target_update = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()
        # Co 3 sekundy ustaw nowy losowy cel dla pszczół
        if current_time - last_target_update > 3000:
            for bee in bees:
                new_target = Vector2D(random.uniform(0, 9), random.uniform(0, 9))
                bee.target = new_target
            last_target_update = current_time

        # Aktualizacja pszczół
        for bee in bees:
            bee.update()

        # Rysowanie
        draw_environment(screen, environment_objects)
        draw_bees(screen, bees)

        pygame.display.flip()
        clock.tick(30)  # 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()