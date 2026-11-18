"""Organización de cursos, unidades temáticas y sesiones de clase."""
from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .actividades import Asistencia, MaterialDidactico, Tarea
    from .evaluaciones import Examen
    from .usuarios import Docente, Estudiante


class Curso:
    def __init__(self, id_curso: str, nombre: str, grado: str):
        self._id_curso = id_curso
        self._nombre = nombre
        self._grado = grado
        self._docente: Docente | None = None            # impartido por 1
        self._estudiantes: list[Estudiante] = []        # 1..*
        self._unidades: list[UnidadTematica] = []       # composición 1..*

    def agregar_unidad(self, id_unidad: str, titulo: str) -> UnidadTematica:
        """Composición: el curso crea y es dueño de sus unidades."""
        unidad = UnidadTematica(id_unidad, titulo, len(self._unidades) + 1)
        self._unidades.append(unidad)
        return unidad

    def _set_docente(self, docente: Docente) -> None:
        self._docente = docente
        docente._asociar_curso(self)

    def _agregar_estudiante(self, estudiante: Estudiante) -> None:
        if estudiante not in self._estudiantes:
            self._estudiantes.append(estudiante)
            estudiante._asociar_curso(self)

    @property
    def id_curso(self) -> str: return self._id_curso
    @property
    def nombre(self) -> str: return self._nombre
    @property
    def grado(self) -> str: return self._grado
    @property
    def docente(self) -> Docente | None: return self._docente
    @property
    def estudiantes(self) -> list[Estudiante]: return list(self._estudiantes)
    @property
    def unidades(self) -> list[UnidadTematica]: return list(self._unidades)



class UnidadTematica:
    def __init__(self, id_unidad: str, titulo: str, orden: int):
        self._id_unidad = id_unidad
        self._titulo = titulo
        self._orden = orden
        self._sesiones: list[SesionClase] = []          # composición 1..*

    def agregar_sesion(self, id_sesion: str, fecha: date, tema: str) -> SesionClase:
        sesion = SesionClase(id_sesion, fecha, tema)
        self._sesiones.append(sesion)
        return sesion

    @property
    def id_unidad(self) -> str: return self._id_unidad
    @property
    def titulo(self) -> str: return self._titulo
    @property
    def orden(self) -> int: return self._orden
    @property
    def sesiones(self) -> list[SesionClase]: return list(self._sesiones)



class SesionClase:
    def __init__(self, id_sesion: str, fecha: date, tema: str):
        self._id_sesion = id_sesion
        self._fecha = fecha
        self._tema = tema
        self._asistencias: list[Asistencia] = []
        self._materiales: list[MaterialDidactico] = []
        self._tareas: list[Tarea] = []
        self._examenes: list[Examen] = []

    def _agregar_asistencia(self, a: Asistencia) -> None: self._asistencias.append(a)
    def _agregar_material(self, m: MaterialDidactico) -> None: self._materiales.append(m)
    def _agregar_tarea(self, t: Tarea) -> None: self._tareas.append(t)
    def _agregar_examen(self, e: Examen) -> None: self._examenes.append(e)

    @property
    def id_sesion(self) -> str: return self._id_sesion
    @property
    def fecha(self) -> date: return self._fecha
    @property
    def tema(self) -> str: return self._tema
    @property
    def asistencias(self) -> list[Asistencia]: return list(self._asistencias)
    @property
    def materiales(self) -> list[MaterialDidactico]: return list(self._materiales)
    @property
    def tareas(self) -> list[Tarea]: return list(self._tareas)
    @property
    def examenes(self) -> list[Examen]: return list(self._examenes)
