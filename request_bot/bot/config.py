import logging
import sys
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN =  os.getenv('BOT_TOKEN')
TELEGRAM_SHARED_SECRET = os.getenv('TELEGRAM_SHARED_SECRET')
API_URL = "http://api_app:8000"

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
log_level = logging.DEBUG
# log_level = logging.INFO

file_handler = RotatingFileHandler(
    os.path.join(log_dir, "bot.log"),
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)
file_handler.setLevel(log_level)
file_handler.setFormatter(logging.Formatter(log_format))

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(log_level)
console_handler.setFormatter(logging.Formatter(log_format))
logging.basicConfig(
    level=log_level,
    format=log_format,
    handlers=[file_handler, console_handler],
)

logger = logging.getLogger(__name__)
