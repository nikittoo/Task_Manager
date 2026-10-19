import pyodbc

SERVIDOR = r".\SQLEXPRESS"
BASE_DE_DATOS = "TaskManagerDB"
DRIVER = "{ODBC Driver 17 for SQL Server}"


def obtener_conexion() -> pyodbc.Connection:
    cadena_conexion = (
        f"DRIVER={DRIVER};"
        f"SERVER={SERVIDOR};"
        f"DATABASE={BASE_DE_DATOS};"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(cadena_conexion)
