from ventanaMain import VentanaDownloader
import logging
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
LOGS_DIR = os.path.join(ROOT_DIR, "logs")

os.makedirs(LOGS_DIR, exist_ok=True)

log_filename = datetime.now().strftime("log_%Y-%m-%d_%H-%M-%S.log")
log_path = os.path.join(LOGS_DIR, log_filename)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

for handler in logger.handlers[:]:
    logger.removeHandler(handler)

file_handler = logging.FileHandler(log_path, encoding="utf-8", mode="w")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.info("Aplicación iniciada correctamente.")
logger.info(f"Archivo de log: {log_path}")

if __name__ == "__main__":
    try:
        app = VentanaDownloader()
        app.run()
    finally:
        for handler in logger.handlers:
            handler.flush()
            handler.close()
