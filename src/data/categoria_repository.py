from typing import List, Optional

from src.data.conexion import obtener_conexion
from src.models.categoria import Categoria


class CategoriaRepository:
    """Acceso de solo lectura a la tabla categorias."""

    def listar_todas(self) -> List[Categoria]:
        consulta = "SELECT * FROM categorias ORDER BY nombre"
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(consulta)
            return [self._fila_a_categoria(fila) for fila in cursor.fetchall()]
        finally:
            conexion.close()

    def obtener_por_id(self, id_categoria: int) -> Optional[Categoria]:
        consulta = "SELECT * FROM categorias WHERE id_categoria = ?"
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(consulta, id_categoria)
            fila = cursor.fetchone()
            return self._fila_a_categoria(fila) if fila else None
        finally:
            conexion.close()

    @staticmethod
    def _fila_a_categoria(fila) -> Categoria:
        return Categoria(
            id_categoria=fila.id_categoria,
            nombre=fila.nombre,
            descripcion=fila.descripcion,
        )
