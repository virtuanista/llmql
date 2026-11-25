import ollama

def generate_sql(query: str) -> str:
    response = ollama.chat(model='qwen2:7b', messages=[
        {'role': 'system', 'content': 'You are a SQL query generator. Translate the following natural language query into a SQL query. The SQL query should start with "SELECT" and be valid SQL syntax.'},
        {'role': 'user', 'content': query}
    ])
    sql = response['message']['content']
    # Comprobación básica de formato (primera capa).
    # La seguridad real la garantiza el usuario de BD de solo lectura.
    if not sql.strip().upper().startswith("SELECT"):
        raise ValueError(f"La respuesta generada no es una consulta SQL válida: {sql}")
    return sql
