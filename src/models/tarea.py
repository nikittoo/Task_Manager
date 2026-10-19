from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from src.models.enums import Estado, Prioridad


@dataclass
class Tarea:
    id_tarea: int
    titulo: str
    id_usuario: int
    descripcion: Optional[str] = None
    prioridad: Prioridad = Prioridad.MEDIA
    fecha_limite: Optional[date] = None
    estado: Estado = Estado.PENDIENTE
    fecha_creacion: Optional[datetime] = None
    id_categoria: Optional[int] = None

    def esta_vencida(self) -> bool:
        if self.fecha_limite is None or self.estado == Estado.COMPLETADA:
            return False
        return self.fecha_limite < date.today()
