<p align="center"><a href="README.md">Español</a> · <b>English</b></p>

# LLMQL

LLMQL is a concept project that queries SQL directly in natural language using a local model that understands Spanish and English, with an emphasis on read-only security.

## Features

- Generation of SQL queries from natural language.
- MySQL connection.
- Database-level security: it connects with a dedicated read-only user, so protection does not depend on validating the query in code.
- Logging and auditing of every generated and executed query.
- Local model: another model can be integrated without much complexity.

## Requirements

- Python 3.12 or later
- MySQL or MariaDB

## Installation

1. Clone the repository:
    ```bash
    $ git clone https://github.com/virtuanista/llmql.git
    $ cd llmql
    ```

2. Install the dependencies:
    ```bash
    $ pip install -r requirements.txt
    ```

3. Create a read-only database user:

    Instead of using `root` or a user with write permissions, create a dedicated user that can only run `SELECT`. That way, even if the model generates a destructive query (`DROP`, `DELETE`, `UPDATE`, `INSERT`...), the database itself will reject it:

    ```sql
    CREATE USER 'llmql_readonly'@'localhost' IDENTIFIED BY 'contraseña_segura';
    GRANT SELECT ON llmql.* TO 'llmql_readonly'@'localhost';
    FLUSH PRIVILEGES;
    ```

    > 💡 If you want to limit the scope further, grant `SELECT` only on the specific tables the assistant should query: `GRANT SELECT ON llmql.ventas TO 'llmql_readonly'@'localhost';`

4. Copy `example.env` to `.env` and set it up with the read-only user:
    ```plaintext
    DB_HOST=localhost
    DB_USER=llmql_readonly
    DB_PASSWORD=contraseña_segura
    DB_NAME=llmql
    ```

## Security

The project's security strategy is based on the principle of least privilege:

- **The database is the barrier, not the code.** Checking in Python that the query starts with `SELECT` is not enough: some queries start with `SELECT` and can still be dangerous (for example `SELECT ... INTO OUTFILE`, or functions with side effects). With a user that only has the `SELECT` privilege, any attempt to write, delete or export fails directly in MySQL.
- **Defense in depth.** The code keeps a basic check of the query format as a first layer, but the real guarantee comes from the read-only user.
- **Auditing.** All generated and executed queries are logged through `logger.py`, so you can review afterwards what SQL the model produced.

## Usage

Run the CLI with a natural language query:

```bash
$ python consulta_cli.py "Ventas del último mes"
```

## Example

Suppose you have a table called `ventas` (sales) and want to know how many sales there were in the last month. You can run the following command:

```bash
$ python consulta_cli.py "¿Cuántas ventas hubo el último mes?"
```

The CLI will generate the corresponding SQL query and return the result:

```plaintext
Generated SQL: SELECT COUNT(*) FROM ventas WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
Result: 150
```

If the model generates something that is not a `SELECT` query, the code rejects it before it reaches the database. And if a query started with `SELECT` but needed more privileges, the database itself would reject it:

```plaintext
Error: La respuesta generada no es una consulta SQL válida: DELETE FROM ventas
```

## Project Structure

```
llmql/
│
├── consulta_cli.py  # Main CLI
├── sql_generator.py # Interaction with the local model
├── db_connector.py  # Secure MySQL connection (read-only user)
├── logger.py        # Logs and auditing (logs/ folder)
├── example.env      # DB configuration template (copied to .env)
├── requirements.txt # Project dependencies
└── README.md        # Project documentation
```

## Changing the AI Model

The project currently uses the `qwen2:7b` model as an example. For it to work, make sure `ollama` is running on your machine with the model installed. You can run the following command to start `ollama` with the `qwen2:7b` model:

```bash
$ ollama run qwen2:7b
```

### Current Code

```python
import ollama

def generate_sql(query: str) -> str:
    response = ollama.chat(model='qwen2:7b', messages=[
        {'role': 'system', 'content': 'You are a SQL query generator. Translate the following natural language query into a SQL query. The SQL query should start with "SELECT" and be valid SQL syntax.'},
        {'role': 'user', 'content': query}
    ])
    sql = response['message']['content']
    # Basic format check (first layer).
    # Real security is guaranteed by the read-only DB user.
    if not sql.strip().upper().startswith("SELECT"):
        raise ValueError(f"La respuesta generada no es una consulta SQL válida: {sql}")
    return sql
```

To change the AI model used to generate SQL queries, simply update the `sql_generator.py` file to use the new model. For example, if you want to use a different model from Hugging Face's `transformers` library, you can do it like this:

```python
from transformers import pipeline

# Load the Hugging Face model
nlp = pipeline("text2sql", model="nombre_del_modelo")

# Generate the SQL query
response = nlp(query)
return response["generated_text"]
```

This approach keeps the project agnostic to the AI model, making it easy to update or change the model by changing only `sql_generator.py`. Because security rests on the read-only database user, changing models does not compromise data integrity.

## License

<p align="center">
	Repository made by <a href="https://github.com/virtuanista" target="_blank">virtu 🎣</a>
</p>

<p align="center">
	<img src="https://open.soniditos.com/cat_footer.svg" />
</p>

<p align="center">
	Copyright &copy; 2025
</p>

<p align="center">
	<a href="LICENSE"><img src="https://img.shields.io/static/v1.svg?style=for-the-badge&label=License&message=MIT&logoColor=d9e0ee&colorA=363a4f&colorB=b7bdf8"/></a>
</p>
