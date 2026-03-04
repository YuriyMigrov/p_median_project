import logging
import sys
from datetime import datetime
import os
from typing import Optional


def setup_logging(log_file: Optional[str] = None) -> logging.Logger:
    """
    Настройка системы логирования

    Args:
        log_file (Optional[str]): путь к файлу для логов. Если None, путь генерируется автоматически

    Returns:
        logger (logging.Logger): настроенный объект логгера
    """

    if log_file is None:
        if not os.path.exists('logs'):
            os.makedirs('logs')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"logs/adjacency_matrix_{timestamp}.log"

    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger('AdjacencyMatrix')
    logger.info(f"Логирование настроено. Файл логов: {log_file}")
    
    return logger

logger = setup_logging()