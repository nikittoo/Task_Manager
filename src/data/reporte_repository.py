from typing import Dict, List

from src.data.conexion import obtener_conexion
from src.data.tarea_repository import TareaRepository
from src.models.tarea import Tarea


class ReporteRepository:
    """Consultas de solo lectura para los reportes resumen."""

    def contar_por_estado(self) -> Dict[str, int]:
        consulta = "SELECT estado, COUNT(*) AS cantidad FROM tareas GROUP BY estado"
        return self._contar(consulta)

    def contar_por_categoria(self) -> Dict[str, int]:
        consulta = """
            SELECT ISNULL(c.nombre, 'Sin categoria') AS categoria, COUNT(*) AS cantidad
            FROM tareas t
            LEFT JOIN categorias c ON c.id_categoria = t.id_categoria
            GROUP BY c.nombre
        """
        return self._contar(consulta)

    def listar_vencidas(self) -> List[Tarea]:
        consulta = """
            SELECT * FROM tareas
            WHERE fecha_limite < CAST(GETDATE() AS DATE)
              AND estado <> 'Completada'
            ORDER BY fecha_limite
        """
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(consulta)
            return [TareaRepository.fila_a_tarea(fila) for fila in cursor.fetchall()]
        finally:
            conexion.close()

    @staticmethod
    def _contar(consulta: str) -> Dict[str, int]:
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(consulta)
            return {fila[0]: fila[1] for fila in cursor.fetchall()}
        finally:
            conexion.close()
