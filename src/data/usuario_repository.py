from typing import List, Optional

from src.data.conexion import obtener_conexion
from src.models.usuario import Usuario


class UsuarioRepository:
    """Acceso de solo lectura a la tabla usuarios."""

    def listar_todos(self) -> List[Usuario]:
        consulta = "SELECT * FROM usuarios ORDER BY nombre_completo"
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(consulta)
            return [self._fila_a_usuario(fila) for fila in cursor.fetchall()]
        finally:
            conexion.close()

    def obtener_por_id(self, id_usuario: int) -> Optional[Usuario]:
        consulta = "SELECT * FROM usuarios WHERE id_usuario = ?"
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(consulta, id_usuario)
            fila = cursor.fetchone()
            return self._fila_a_usuario(fila) if fila else None
        finally:
            conexion.close()

    @staticmethod
    def _fila_a_usuario(fila) -> Usuario:
        return Usuario(
            id_usuario=fila.id_usuario,
            nombre_usuario=fila.nombre_usuario,
            nombre_completo=fila.nombre_completo,
            email=fila.email,
            fecha_registro=fila.fecha_registro,
        )
