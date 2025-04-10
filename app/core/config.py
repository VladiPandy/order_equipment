import os
import logging.config
from typing import List

# Настройки логирования
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'json': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 10485760,  # 10 МБ
            'backupCount': 5,  # Сохраняем 5 последних логов
        },
    },
    'loggers': {
        '': {  # Корневой логгер
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'uvicorn': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'sqlalchemy': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Применяем настройки логирования
try:
    os.makedirs('logs', exist_ok=True)  # Создаем директорию для логов, если ее нет
    logging.config.dictConfig(LOGGING_CONFIG)
except Exception as e:
    print(f"Ошибка настройки логирования: {e}")

# Настройки приложения 