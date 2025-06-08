import logging
import os
from datetime import datetime

class LogEmoji:
    BEE = "🐝"
    FLOWER = "🌸"
    HIVE = "🏠"

    @staticmethod
    def get_emoji(entity_type: str) -> str:
        if "bee" in entity_type.lower():
            return LogEmoji.BEE
        elif "flower" in entity_type.lower():
            return LogEmoji.FLOWER
        elif "hive" in entity_type.lower():
            return LogEmoji.HIVE
        return ""

class LoggerSubject:
    def __init__(self):
        self.observers = []
    def attach(self, observer):
        self.observers.append(observer)
    def detach(self, observer):
        self.observers.remove(observer)
    def notify(self, message):
        for observer in self.observers:
            observer.update(message)

class FileLogger:
    def __init__(self, entity_type, entity_id):
        self.logger = logging.getLogger(f"{entity_type}_{entity_id}")
        self.entity_type = entity_type
        self.logger.setLevel(logging.INFO)
        log_dir = os.path.join('logs', 'entities', entity_type, str(entity_id))
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%S%M%H_%d%m%Y")
        log_file = os.path.join(log_dir, f'log_{timestamp}.log')
        handler = logging.FileHandler(log_file, encoding='utf-8')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - [%(message)s]')
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def update(self, message):
        try:
            emoji = LogEmoji.get_emoji(self.entity_type)
            self.logger.info(f"{emoji} {message}")
        except Exception:
            self.logger.info(message)

class ConsoleLogger:
    def __init__(self, entity_type):
        self.entity_type = entity_type

    def update(self, message):
        try:
            emoji = LogEmoji.get_emoji(self.entity_type)
            print(f"{emoji} {message}", flush=True)
        except Exception:
            print(message, flush=True)
