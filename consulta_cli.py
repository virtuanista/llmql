import typer
from sql_generator import generate_sql
from db_connector import execute_query
from logger import log_query
import logging

app = typer.Typer()

logging.basicConfig(level=logging.DEBUG)

@app.command()
def consulta(query: str = typer.Option(..., prompt="¿Qué te gustaría consultar?")):
    logging.debug(f'Received query: {query}')
    try:
        sql = generate_sql(query)
        logging.debug(f'Generated SQL: {sql}')
        if not sql.strip().upper().startswith("SELECT"):
            raise ValueError(f"¡Prohibido ejecutar consultas que no sean SELECT! Respuesta generada: {sql}")
        result = execute_query(sql)
        logging.debug(f'Query result: {result}')
        log_query(query, sql)
        print(result)  # Mostrar el resultado en la consola
    except ValueError as e:
        logging.error(e)
        print(e)

if __name__ == "__main__":
    app()