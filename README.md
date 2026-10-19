# Sistema de Gestión de Tareas Personales (Task Manager)

Aplicación de consola en Python para gestionar tareas personales, con persistencia
en una base de datos relacional SQL Server. Proyecto hecho con fines de portfolio,
con foco en arquitectura orientada a objetos y buenas prácticas de acceso a datos.

## Descripción

Permite crear, listar, editar y eliminar tareas, asignarlas a un usuario y a una
categoría, definir prioridad y fecha límite, filtrar por estado, y generar reportes
resumen (cantidad de tareas por estado, por categoría, y tareas vencidas).

## Tecnologías

- **Python 3.12**
- **SQL Server** (Express) como motor de base de datos
- **pyodbc** para la conexión, con **Windows Authentication**
- **ODBC Driver 17 for SQL Server**

## Arquitectura

El proyecto separa responsabilidades en tres capas:

```
TaskManager/
├── sql/
│   └── schema.sql              # Creación de la base, tablas y datos de ejemplo
├── src/
│   ├── models/                 # Clases de dominio (sin lógica de SQL)
│   │   ├── enums.py             # Prioridad y Estado
│   │   ├── usuario.py
│   │   ├── categoria.py
│   │   └── tarea.py
│   ├── data/                   # Acceso a datos (un repositorio por tabla)
│   │   ├── conexion.py          # Conexión pyodbc con Windows Authentication
│   │   ├── usuario_repository.py
│   │   ├── categoria_repository.py
│   │   ├── tarea_repository.py  # CRUD completo de tareas
│   │   └── reporte_repository.py
│   ├── menu.py                  # Menú interactivo de consola
│   └── main.py                  # Punto de entrada
├── requirements.txt
└── README.md
```

- **`models`**: clases de datos (`dataclass`) que representan cada fila de la base,
  sin saber nada de SQL.
- **`data`**: un repositorio por tabla, con consultas parametrizadas (`?`) para
  evitar SQL injection, y responsable de abrir/cerrar la conexión.
- **`menu.py`**: orquesta la interacción con el usuario llamando a los repositorios;
  no contiene SQL.

## Modelo de base de datos

Tres tablas:

- **`usuarios`**: datos de cada usuario.
- **`categorias`**: categorías para clasificar tareas (Estudio, Trabajo, Personal, etc.).
- **`tareas`**: título, descripción, prioridad (`Alta`/`Media`/`Baja`), fecha límite,
  estado (`Pendiente`/`En progreso`/`Completada`), y claves foráneas hacia
  `usuarios` (obligatoria) y `categorias` (opcional).

El script [`sql/schema.sql`](sql/schema.sql) crea la base `TaskManagerDB`, las
tablas con sus restricciones (`PRIMARY KEY`, `FOREIGN KEY`, `CHECK`), e inserta
datos de ejemplo para poder probar la app apenas se crea la base.

## Instalación y uso

### Requisitos previos

- Python 3.12+
- SQL Server (Express o superior) con una instancia accesible localmente
- [ODBC Driver 17 for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)

### Pasos

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/nikittoo/Task_Manager.git
   cd Task_Manager
   ```

2. Crear y activar un entorno virtual:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecutar el script [`sql/schema.sql`](sql/schema.sql) en SQL Server (desde SSMS,
   Azure Data Studio o la extensión SQL Server de VS Code) para crear la base de
   datos `TaskManagerDB` con sus tablas y datos de ejemplo.

5. Revisar [`src/data/conexion.py`](src/data/conexion.py) y ajustar `SERVIDOR` con
   el nombre de tu instancia de SQL Server (por defecto `.\SQLEXPRESS`).

6. Ejecutar la aplicación:

   ```bash
   python -m src.main
   ```

## Funcionalidades

- CRUD completo de tareas (crear, listar, editar, eliminar)
- Prioridades (Alta / Media / Baja)
- Fechas límite
- Filtrado de tareas por estado (Pendiente / En progreso / Completada)
- Reportes resumen: cantidad de tareas por estado, por categoría, y tareas vencidas

## Capturas de pantalla

_Pendiente: se agregan una vez que la base de datos esté levantada y la app
probada de punta a punta._

## Posibles mejoras futuras

- Tests automatizados (unitarios para los repositorios con una base de pruebas)
- Validaciones adicionales de entrada en el menú
- Exportar reportes a CSV

## Autor

Proyecto desarrollado como parte de mi portfolio personal, estudiante de
Ingeniería Informática.
