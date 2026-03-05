import logging
import sys
from datetime import datetime
from typing import Optional
from pathlib import Path


def get_base_path() -> Path:
    """Определяет папку программы"""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


def setup_logging(log_file: Optional[Path] = None) -> logging.Logger:
    """
    Настройка системы логирования

    Args:
        log_file (Optional[str]): путь к файлу для логов. Если None, путь генерируется автоматически

    Returns:
        logger (logging.Logger): настроенный объект логгера
    """

    BASE_DIR = get_base_path()
    logs_dir = BASE_DIR / "logs"

    logs_dir.mkdir(exist_ok=True)

    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = logs_dir / f"adjacency_matrix_{timestamp}.log"

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger('PMedianProject')
    logger.info(f"Логирование настроено. Файл логов: {log_file}")
    
    return logger

logger = setup_logging()