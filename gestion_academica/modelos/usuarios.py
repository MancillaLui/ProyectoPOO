"""Usuarios, autenticación y operaciones de cada rol."""
from __future__ import annotations

from abc import ABC
from datetime import date
from typing import TYPE_CHECKING

from .actividades import Asistencia, EntregaTarea, MaterialDidactico, Tarea
from .evaluaciones import Examen, RendicionExamen

if TYPE_CHECKING:
    from .academico import Curso, SesionClase


class Usuario(ABC):
    """Clase abstracta: identidad común a todo usuario de la plataforma."""

    def __init__(self, codigo_institucional: str, nombre: str, apellido: str,
                 correo: str, contrasenia: str):
        self._codigo_institucional = codigo_institucional
        self._nombre = nombre
        self._apellido = apellido
        self._correo = correo
        self._contrasenia = contrasenia

    def autenticar(self, codigo: str, contrasenia: str) -> bool:
        return self._codigo_institucional == codigo and self._contrasenia == contrasenia

    def cambiar_contrasenia(self, actual: str, nueva: str) -> None:
        if self._contrasenia != actual:
            raise ValueError("La contraseña actual es incorrecta")
        self._contrasenia = nueva

    @property
    def codigo_institucional(self) -> str: return self._codigo_institucional
    @property
    def nombre(self) -> str: return self._nombre
    @property
    def apellido(self) -> str: return self._apellido
    @property
    def correo(self) -> str: return self._correo

    def __str__(self) -> str:
        return f"{self._nombre} {self._apellido} ({self._codigo_institucional})"



class Docente(Usuario):
    def __init__(self, codigo_institucional, nombre, apellido, correo, contrasenia,
                 especialidad: str):
        super().__init__(codigo_institucional, nombre, apellido, correo, contrasenia)
        self._especialidad = especialidad
        self._cursos: list[Curso] = []          # imparte 1..*

    def publicar_material(self, sesion: SesionClase, id_material: str, titulo: str,
                          tipo_formato: str, url_archivo: str) -> MaterialDidactico:
        material = MaterialDidactico(id_material, titulo, tipo_formato, url_archivo)
        sesion._agregar_material(material)
        return material

    def crear_tarea(self, sesion: SesionClase, id_tarea: str, titulo: str,
                    descripcion: str, fecha_limite: date) -> Tarea:
        tarea = Tarea(id_tarea, titulo, descripcion, fecha_limite)
        sesion._agregar_tarea(tarea)
        return tarea

    def crear_examen(self, sesion: SesionClase, id_examen: str, titulo: str,
                     duracion_minutos: int) -> Examen:
        examen = Examen(id_examen, titulo, duracion_minutos)
        sesion._agregar_examen(examen)
        return examen

    def registrar_asistencia(self, sesion: SesionClase, estudiante: Estudiante,
                             estado: str) -> Asistencia:
        asistencia = Asistencia(f"AS-{len(sesion.asistencias) + 1}", date.today(),
                                estado, estudiante)
        sesion._agregar_asistencia(asistencia)
        return asistencia

    def _asociar_curso(self, curso: Curso) -> None:
        if curso not in self._cursos:
            self._cursos.append(curso)

    @property
    def especialidad(self) -> str: return self._especialidad
    @property
    def cursos(self) -> list[Curso]: return list(self._cursos)



class Estudiante(Usuario):
    def __init__(self, codigo_institucional, nombre, apellido, correo, contrasenia,
                 grado: str, seccion: str):
        super().__init__(codigo_institucional, nombre, apellido, correo, contrasenia)
        self._grado = grado
        self._seccion = seccion
        self._cursos: list[Curso] = []          # matriculado 0..*

    def ver_cursos(self) -> list[Curso]:
        return list(self._cursos)

    def entregar_tarea(self, tarea: Tarea, archivo_enviado: str) -> EntregaTarea:
        entrega = EntregaTarea(f"EN-{len(tarea.entregas) + 1}", archivo_enviado, self, tarea)
        entrega.enviar()
        return entrega

    def rendir_examen(self, examen: Examen) -> RendicionExamen:
        """Inicia la rendición; las respuestas se registran con RendicionExamen.responder()."""
        rendicion = RendicionExamen(f"RE-{len(examen.rendiciones) + 1}", self, examen)
        examen._registrar_rendicion(rendicion)
        return rendicion

    def _asociar_curso(self, curso: Curso) -> None:
        if curso not in self._cursos:
            self._cursos.append(curso)

    @property
    def grado(self) -> str: return self._grado
    @property
    def seccion(self) -> str: return self._seccion



class Administrador(Usuario):
    def __init__(self, codigo_institucional, nombre, apellido, correo, contrasenia,
                 nivel_acceso: str):
        super().__init__(codigo_institucional, nombre, apellido, correo, contrasenia)
        self._nivel_acceso = nivel_acceso

    def gestionar_usuarios(self, registro: list[Usuario], nuevo: Usuario) -> None:
        if any(u.codigo_institucional == nuevo.codigo_institucional for u in registro):
            raise ValueError("Ya existe un usuario con ese código")
        registro.append(nuevo)

    def asignar_docente(self, docente: Docente, curso: Curso) -> None:
        curso._set_docente(docente)

    def matricular_estudiante(self, estudiante: Estudiante, curso: Curso) -> None:
        """En el diagrama original figura como 'mecularEstudiante()' (typo)."""
        curso._agregar_estudiante(estudiante)

    @property
    def nivel_acceso(self) -> str: return self._nivel_acceso
