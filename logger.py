import logging
from pathlib import Path

LOGS = Path(__file__).with_name('logs')
LOGS.mkdir(exist_ok=True)


def _logger(name: str) -> logging.Logger:
    log = logging.getLogger(f'llmql.{name}')
    if not log.handlers:
        handler = logging.FileHandler(LOGS / f'{name}.log', encoding='utf-8')
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        log.addHandler(handler)
        log.setLevel(logging.INFO)
        log.propagate = False
    return log


consultas = _logger('consultas')
db_errors = _logger('db_errors')


def log_query(query: str, sql: str):
    consultas.info(f'Entrada: "{query}"')
    consultas.info(f'SQL Generado: {sql}')
