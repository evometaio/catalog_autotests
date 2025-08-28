import logging
import os
from datetime import datetime


def setup_logger(name: str = "autotests", level: str = "INFO") -> logging.Logger:
    """
    Настраивает и возвращает логгер.
    
    Args:
        name: Имя логгера
        level: Уровень логирования
        
    Returns:
        Настроенный логгер
    """
    logger = logging.getLogger(name)
    
    if logger.handlers:  # Логгер уже настроен
        return logger
    
    # Уровень логирования
    logger.setLevel(getattr(logging, level.upper()))
    
    # Создаем директорию для логов если её нет
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Форматтер
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)
    
    # Хендлер для файла
    log_file = os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Хендлер для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = "autotests") -> logging.Logger:
    """
    Возвращает логгер с указанным именем.
    
    Args:
        name: Имя логгера
        
    Returns:
        Логгер
    """
    return logging.getLogger(name)


# Основной логгер
logger = get_logger()
