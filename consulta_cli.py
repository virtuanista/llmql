import typer

from db_connector import execute_query
from logger import log_query
from sql_generator import generate_sql

app = typer.Typer()


@app.command()
def consulta(query: str = typer.Argument(None, help="Pregunta en lenguaje natural.")):
    if not query:
        query = typer.prompt("¿Qué te gustaría consultar?")
    try:
        sql = generate_sql(query)
        log_query(query, sql)
        print(f"Generated SQL: {sql}")
        result = execute_query(sql)
        # Un único valor se muestra sin la tupla que lo envuelve.
        print(f"Result: {result[0][0] if len(result) == 1 and len(result[0]) == 1 else result}")
    except Exception as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
