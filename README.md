# LLMQL

LLMQL es un concepto de proyecto que consulta SQL directamente con lenguaje natural utilizando un modelo local que entiende español e inglés, con énfasis en seguridad de solo lectura.

## Características

- Generación de consultas SQL a partir de lenguaje natural.
- Conexión a MySQL.
- Seguridad a nivel de base de datos: se conecta con un usuario dedicado de solo lectura, por lo que la protección no depende de validar la consulta en el código.
- Registro y auditoría de cada consulta generada y ejecutada.
- Modelo local: permite integrar otro modelo de manera no muy compleja.

## Requisitos

- Python 3.12 o superior
- MySQL o MariaDB

## Instalación

1. Clona el repositorio:
    ```bash
    $ git clone https://github.com/virtuanista/llmql.git
    $ cd llmql
    ```

2. Instala las dependencias:
    ```bash
    $ pip install -r requirements.txt
    ```

3. Crea un usuario de base de datos de solo lectura:

    En lugar de usar `root` o un usuario con permisos de escritura, crea un usuario dedicado que solo pueda ejecutar `SELECT`. Así, aunque el modelo genere una consulta destructiva (`DROP`, `DELETE`, `UPDATE`, `INSERT`...), la propia base de datos la rechazará:

    ```sql
    CREATE USER 'llmql_readonly'@'localhost' IDENTIFIED BY 'contraseña_segura';
    GRANT SELECT ON llmql.* TO 'llmql_readonly'@'localhost';
    FLUSH PRIVILEGES;
    ```

    > 💡 Si quieres limitar aún más el alcance, concede `SELECT` solo sobre las tablas concretas que el asistente deba consultar: `GRANT SELECT ON llmql.ventas TO 'llmql_readonly'@'localhost';`

4. Configura las variables de entorno en el archivo `.env` con el usuario de solo lectura:
    ```plaintext
    DB_HOST=localhost
    DB_USER=llmql_readonly
    DB_PASSWORD=contraseña_segura
    DB_NAME=llmql
    ```

## Seguridad

La estrategia de seguridad del proyecto se basa en el principio de mínimo privilegio:

- **La base de datos es la barrera, no el código.** Validar en Python que la consulta empiece por `SELECT` es insuficiente: existen consultas que empiezan por `SELECT` y aun así pueden ser peligrosas (por ejemplo `SELECT ... INTO OUTFILE`, o funciones con efectos secundarios). Con un usuario que solo tiene el privilegio `SELECT`, cualquier intento de escritura, borrado o exportación falla directamente en MySQL.
- **Defensa en profundidad.** El código mantiene una comprobación básica del formato de la consulta como primera capa, pero la garantía real la aporta el usuario de solo lectura.
- **Auditoría.** Todas las consultas generadas y ejecutadas quedan registradas mediante `logger.py`, lo que permite revisar a posteriori qué SQL ha producido el modelo.

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

Si el modelo generase una consulta no permitida, la base de datos la rechazará por falta de privilegios:

```plaintext
Generated SQL: DELETE FROM ventas
Error: (1142, "DELETE command denied to user 'llmql_readonly'@'localhost' for table 'ventas'")
```

## Estructura del Proyecto

```
llmql/
│
├── consulta_cli.py  # CLI principal
├── sql_generator.py # Interacción con el modelo local
├── db_connector.py  # Conexión segura a MySQL (usuario de solo lectura)
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
    # Comprobación básica de formato (primera capa).
    # La seguridad real la garantiza el usuario de BD de solo lectura.
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

Este enfoque permite que el proyecto sea agnóstico al modelo de IA, facilitando la actualización o el cambio del modelo sin necesidad de modificar el código base. Gracias a que la seguridad recae en el usuario de solo lectura de la base de datos, cambiar de modelo no compromete la integridad de los datos.

## Licencia

<p align="center">
	Repositorio generado por <a href="https://github.com/virtuanista" target="_blank">virtu 🎣</a>
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
