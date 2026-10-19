from typing import List, Optional

from src.data.conexion import obtener_conexion
from src.models.enums import Estado, Prioridad
from src.models.tarea import Tarea


class TareaRepository:
    """Acceso a datos para la tabla tareas (CRUD)."""

    def crear(self, tarea: Tarea) -> int:
        consulta = """
            INSERT INTO tareas (titulo, descripcion, prioridad, fecha_limite, estado, id_usuario, id_categoria)
            OUTPUT INSERTED.id_tarea
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                consulta,
                tarea.titulo,
                tarea.descripcion,
                tarea.prioridad.value,
                tarea.fecha_limite,
                tarea.estado.value,
                tarea.id_usuario,
                tarea.id_categoria,
            )
            nuevo_id = cursor.fetchone()[0]
            conexion.commit()
            return nuevo_id
        finally:
            conexion.close()

    def obtener_por_id(self, id_tarea: int) -> Optional[Tarea]:
        consulta = "SELECT * FROM tareas WHERE id_tarea = ?"
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(consulta, id_tarea)
            fila = cursor.fetchone()
            return self.fila_a_tarea(fila) if fila else None
        finally:
            conexion.close()

    def listar_todas(self) -> List[Tarea]:
        consulta = "SELECT * FROM tareas ORDER BY fecha_limite"
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(consulta)
            return [self.fila_a_tarea(fila) for fila in cursor.fetchall()]
        finally:
            conexion.close()

    def listar_por_estado(self, estado: Estado) -> List[Tarea]:
        consulta = "SELECT * FROM tareas WHERE estado = ? ORDER BY fecha_limite"
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(consulta, estado.value)
            return [self.fila_a_tarea(fila) for fila in cursor.fetchall()]
        finally:
            conexion.close()

    def actualizar(self, tarea: Tarea) -> bool:
        consulta = """
            UPDATE tareas
            SET titulo = ?, descripcion = ?, prioridad = ?, fecha_limite = ?,
                estado = ?, id_usuario = ?, id_categoria = ?
            WHERE id_tarea = ?
        """
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(
                consulta,
                tarea.titulo,
                tarea.descripcion,
                tarea.prioridad.value,
                tarea.fecha_limite,
                tarea.estado.value,
                tarea.id_usuario,
                tarea.id_categoria,
                tarea.id_tarea,
            )
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            conexion.close()

    def eliminar(self, id_tarea: int) -> bool:
        consulta = "DELETE FROM tareas WHERE id_tarea = ?"
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(consulta, id_tarea)
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            conexion.close()

    @staticmethod
    def fila_a_tarea(fila) -> Tarea:
        return Tarea(
            id_tarea=fila.id_tarea,
            titulo=fila.titulo,
            descripcion=fila.descripcion,
            prioridad=Prioridad(fila.prioridad),
            fecha_limite=fila.fecha_limite,
            estado=Estado(fila.estado),
            fecha_creacion=fila.fecha_creacion,
            id_usuario=fila.id_usuario,
            id_categoria=fila.id_categoria,
        )
