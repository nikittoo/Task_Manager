from datetime import datetime

from src.data.categoria_repository import CategoriaRepository
from src.data.reporte_repository import ReporteRepository
from src.data.tarea_repository import TareaRepository
from src.data.usuario_repository import UsuarioRepository
from src.models.enums import Estado, Prioridad
from src.models.tarea import Tarea


class Menu:
    """Menu interactivo de consola. Orquesta los repositorios, sin logica de SQL."""

    def __init__(self):
        self.tarea_repo = TareaRepository()
        self.usuario_repo = UsuarioRepository()
        self.categoria_repo = CategoriaRepository()
        self.reporte_repo = ReporteRepository()

    def iniciar(self):
        acciones = {
            "1": self.listar_tareas,
            "2": self.crear_tarea,
            "3": self.editar_tarea,
            "4": self.eliminar_tarea,
            "5": self.filtrar_por_estado,
            "6": self.mostrar_reportes,
        }
        while True:
            self._mostrar_opciones()
            opcion = input("Elegi una opcion: ").strip()
            if opcion == "0":
                print("Hasta luego!")
                break
            accion = acciones.get(opcion)
            if accion is None:
                print("Opcion invalida.\n")
                continue
            try:
                accion()
            except Exception as error:
                print(f"Ocurrio un error: {error}\n")

    @staticmethod
    def _mostrar_opciones():
        print("\n===== Gestor de Tareas =====")
        print("1. Listar tareas")
        print("2. Crear tarea")
        print("3. Editar tarea")
        print("4. Eliminar tarea")
        print("5. Filtrar tareas por estado")
        print("6. Reportes")
        print("0. Salir")

    # ---------- opciones del menu ----------

    def listar_tareas(self):
        self._imprimir_tareas(self.tarea_repo.listar_todas())

    def crear_tarea(self):
        print("\n-- Nueva tarea --")
        titulo = input("Titulo: ").strip()
        descripcion = input("Descripcion (opcional): ").strip() or None

        id_usuario = self._elegir_usuario()
        if id_usuario is None:
            print("No se puede crear una tarea sin usuario.\n")
            return
        id_categoria = self._elegir_categoria()
        prioridad = self._elegir_opcion_enum("Prioridad", Prioridad)
        fecha_limite = self._pedir_fecha("Fecha limite (DD/MM/AAAA, opcional): ")

        tarea = Tarea(
            id_tarea=0,
            titulo=titulo,
            descripcion=descripcion,
            prioridad=prioridad,
            fecha_limite=fecha_limite,
            estado=Estado.PENDIENTE,
            id_usuario=id_usuario,
            id_categoria=id_categoria,
        )
        nuevo_id = self.tarea_repo.crear(tarea)
        print(f"Tarea creada con id {nuevo_id}.\n")

    def editar_tarea(self):
        id_tarea = self._pedir_entero("Id de la tarea a editar: ")
        tarea = self.tarea_repo.obtener_por_id(id_tarea)
        if tarea is None:
            print("No existe una tarea con ese id.\n")
            return

        print("Dejar vacio para mantener el valor actual.")

        nuevo_titulo = input(f"Titulo [{tarea.titulo}]: ").strip()
        tarea.titulo = nuevo_titulo or tarea.titulo

        nueva_descripcion = input(f"Descripcion [{tarea.descripcion or '-'}]: ").strip()
        tarea.descripcion = nueva_descripcion or tarea.descripcion

        print(f"Estado actual: {tarea.estado.value}")
        cambiar_estado = input("Cambiar estado? (s/n): ").strip().lower()
        if cambiar_estado == "s":
            tarea.estado = self._elegir_opcion_enum("Estado", Estado)

        actualizado = self.tarea_repo.actualizar(tarea)
        print("Tarea actualizada.\n" if actualizado else "No se pudo actualizar la tarea.\n")

    def eliminar_tarea(self):
        id_tarea = self._pedir_entero("Id de la tarea a eliminar: ")
        confirmacion = input("Seguro que queres eliminarla? (s/n): ").strip().lower()
        if confirmacion != "s":
            print("Operacion cancelada.\n")
            return
        eliminado = self.tarea_repo.eliminar(id_tarea)
        print("Tarea eliminada.\n" if eliminado else "No existe una tarea con ese id.\n")

    def filtrar_por_estado(self):
        estado = self._elegir_opcion_enum("Estado", Estado)
        self._imprimir_tareas(self.tarea_repo.listar_por_estado(estado))

    def mostrar_reportes(self):
        print("\n-- Tareas por estado --")
        for estado, cantidad in self.reporte_repo.contar_por_estado().items():
            print(f"  {estado}: {cantidad}")

        print("\n-- Tareas por categoria --")
        for categoria, cantidad in self.reporte_repo.contar_por_categoria().items():
            print(f"  {categoria}: {cantidad}")

        print("\n-- Tareas vencidas --")
        self._imprimir_tareas(self.reporte_repo.listar_vencidas())

    # ---------- helpers de entrada ----------

    def _elegir_usuario(self):
        usuarios = self.usuario_repo.listar_todos()
        if not usuarios:
            print("No hay usuarios cargados en la base.")
            return None
        print("Usuarios disponibles:")
        for usuario in usuarios:
            print(f"  {usuario.id_usuario}. {usuario.nombre_completo} ({usuario.nombre_usuario})")
        return self._pedir_entero("Id de usuario: ")

    def _elegir_categoria(self):
        categorias = self.categoria_repo.listar_todas()
        if not categorias:
            return None
        print("Categorias disponibles (dejar vacio = sin categoria):")
        for categoria in categorias:
            print(f"  {categoria.id_categoria}. {categoria.nombre}")
        entrada = input("Id de categoria: ").strip()
        return int(entrada) if entrada.isdigit() else None

    @staticmethod
    def _elegir_opcion_enum(etiqueta, enum_clase):
        valores = list(enum_clase)
        print(f"{etiqueta}:")
        for indice, valor in enumerate(valores, start=1):
            print(f"  {indice}. {valor.value}")
        while True:
            entrada = input("Elegi una opcion: ").strip()
            if entrada.isdigit() and 1 <= int(entrada) <= len(valores):
                return valores[int(entrada) - 1]
            print("Opcion invalida.")

    @staticmethod
    def _pedir_fecha(mensaje):
        entrada = input(mensaje).strip()
        if not entrada:
            return None
        try:
            return datetime.strptime(entrada, "%d/%m/%Y").date()
        except ValueError:
            print("Fecha invalida, se guarda sin fecha limite.")
            return None

    @staticmethod
    def _pedir_entero(mensaje):
        while True:
            entrada = input(mensaje).strip()
            if entrada.isdigit():
                return int(entrada)
            print("Tenes que ingresar un numero.")

    @staticmethod
    def _imprimir_tareas(tareas):
        if not tareas:
            print("No hay tareas para mostrar.\n")
            return
        for tarea in tareas:
            marca_vencida = " (VENCIDA)" if tarea.esta_vencida() else ""
            fecha = tarea.fecha_limite.strftime("%d/%m/%Y") if tarea.fecha_limite else "sin fecha"
            print(
                f"[{tarea.id_tarea}] {tarea.titulo} - {tarea.prioridad.value} "
                f"- {tarea.estado.value} - vence {fecha}{marca_vencida}"
            )
        print()
