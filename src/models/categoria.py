from dataclasses import dataclass
from typing import Optional


@dataclass
class Categoria:
    id_categoria: int
    nombre: str
    descripcion: Optional[str] = None
