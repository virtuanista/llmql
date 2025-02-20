import logging

logging.basicConfig(filename='logs/consultas.log', level=logging.INFO)

def log_query(query: str, sql: str):
    logging.info(f'Entrada: "{query}"')
    logging.info(f'SQL Generado: {sql}')