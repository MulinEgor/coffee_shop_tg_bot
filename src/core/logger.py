import logging


def get_logger(name: str) -> logging.Logger:
    """
    Получение дефолтного логгера.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # Логирование в файл
    # handler = logging.FileHandler('logs.txt', mode='w')
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)

    # Логирование в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
