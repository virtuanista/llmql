# LLMQL

LLMQL es concepto de proyecto que consulta SQL directamente con lenguaje natural utilizando un modelo local que entiende español e inglés, con énfasis en seguridad de solo lectura.

## Características

- Generación de consultas SQL a partir de lenguaje natural.
- Conexión a MySQL.
- Registro y auditoría de cada consulta generada y ejecutada.
- Modelo local: Permite integrar otro modelo de manera no muy compleja.

## Requisitos

- Python 3.12 o superior
- MySQL o MariaDB

## Instalación

1. Clona el repositorio:

    ```bash
    $ git clone https://github.com/sabiopobre/llmql.git
    $ cd llmql
    ```

2. Instala las dependencias:

    ```bash
    $ pip install -r requirements.txt
    ```

3. Configura las variables de entorno en el archivo `.env`:

    ```plaintext
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=your_password
    DB_NAME=llmql
    ```

## Uso

Ejecuta la CLI con una consulta en lenguaje natural:

```bash
$ python consulta_cli.py "Ventas del último mes"
```

## Ejemplo

Supongamos que tienes una tabla llamada `ventas` y quieres saber cuántas ventas hubo el último mes. Puedes ejecutar el siguiente comando:

```bash
$ python consulta_cli.py "¿Cuántas ventas hubo el último mes?"
```

La CLI generará la consulta SQL correspondiente y devolverá el resultado:

```plaintext
Generated SQL: SELECT COUNT(*) FROM ventas WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
Result: 150
```

## Estructura del Proyecto

```
llmql/
│
├── consulta_cli.py  # CLI principal
├── sql_generator.py # Interacción con el modelo local
├── db_connector.py  # Conexión segura a MySQL
├── logger.py        # Logs y auditoría
├── .env             # Configuración de BD
├── requirements.txt # Dependencias del proyecto
└── README.md        # Documentación del proyecto
```

## Cambiar el Modelo de IA

Actualmente, el proyecto utiliza el modelo `qwen2:7b` a modo de ejemplo. Para que funcione, asegúrate de tener `ollama` activo en tu equipo con el modelo instalado. Puedes ejecutar el siguiente comando para iniciar `ollama` con el modelo `qwen2:7b`:

```bash
$ ollama run qwen2:7b
```

### Código Actual

```python
import ollama

def generate_sql(query: str) -> str:
    response = ollama.chat(model='qwen2:7b', messages=[
        {'role': 'system', 'content': 'You are a SQL query generator. Translate the following natural language query into a SQL query. The SQL query should start with "SELECT" and be valid SQL syntax.'},
        {'role': 'user', 'content': query}
    ])
    sql = response['message']['content']
    if not sql.strip().upper().startswith("SELECT"):
        raise ValueError(f"La respuesta generada no es una consulta SQL válida: {sql}")
    return sql
```

Para cambiar el modelo de IA utilizado para generar consultas SQL, simplemente actualiza el archivo `sql_generator.py` para utilizar el nuevo modelo. Por ejemplo, si deseas utilizar un modelo diferente de la biblioteca `transformers` de Hugging Face, puedes hacerlo de la siguiente manera:

```python
from transformers import pipeline

# Cargar el modelo de Hugging Face
nlp = pipeline("text2sql", model="nombre_del_modelo")

# Generar la consulta SQL
response = nlp(query)
return response["generated_text"]
```

Este enfoque permite que el proyecto sea agnóstico al modelo de IA, facilitando la actualización o el cambio del modelo sin necesidad de modificar el código base.

## Licencia

<p align="center">
	Repositorio generado por <a href="https://github.com/sabiopobre" target="_blank">virtu 🎣</a>
</p>

<p align="center">
	<img src="https://open.soniditos.com/cat_footer.svg" />
</p>

<p align="center">
	Copyright &copy; 2025
</p>

<p align="center">
	<a href="/LICENSE"><img src="https://img.shields.io/static/v1.svg?style=for-the-badge&label=License&message=MIT&logoColor=d9e0ee&colorA=363a4f&colorB=b7bdf8"/></a>
</p>
