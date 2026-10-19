from dataclasses import dataclass
from datetime import datetime


@dataclass
class Usuario:
    id_usuario: int
    nombre_usuario: str
    nombre_completo: str
    email: str
    fecha_registro: datetime
