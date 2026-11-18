"""Asistencias, materiales didácticos, tareas y entregas."""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .usuarios import Estudiante


class Asistencia:
    def __init__(self, id_asistencia: str, fecha: date, estado: str, estudiante: Estudiante):
        self._id_asistencia = id_asistencia
        self._fecha = fecha
        self._estado = estado               # PRESENTE, AUSENTE, TARDANZA...
        self._estudiante = estudiante       # añadido: sin él el registro carece de sentido

    @property
    def id_asistencia(self) -> str: return self._id_asistencia
    @property
    def fecha(self) -> date: return self._fecha
    @property
    def estado(self) -> str: return self._estado
    @property
    def estudiante(self) -> Estudiante: return self._estudiante



class MaterialDidactico:
    def __init__(self, id_material: str, titulo: str, tipo_formato: str, url_archivo: str):
        self._id_material = id_material
        self._titulo = titulo
        self._tipo_formato = tipo_formato
        self._url_archivo = url_archivo

    def descargar(self) -> Path:
        return Path(self._url_archivo)

    @property
    def id_material(self) -> str: return self._id_material
    @property
    def titulo(self) -> str: return self._titulo
    @property
    def tipo_formato(self) -> str: return self._tipo_formato
    @property
    def url_archivo(self) -> str: return self._url_archivo



class Tarea:
    def __init__(self, id_tarea: str, titulo: str, descripcion: str, fecha_limite: date):
        self._id_tarea = id_tarea
        self._titulo = titulo
        self._descripcion = descripcion
        self._fecha_limite = fecha_limite
        self._entregas: list[EntregaTarea] = []         # recibe 0..*

    def _registrar_entrega(self, entrega: EntregaTarea) -> None:
        self._entregas.append(entrega)

    @property
    def id_tarea(self) -> str: return self._id_tarea
    @property
    def titulo(self) -> str: return self._titulo
    @property
    def descripcion(self) -> str: return self._descripcion
    @property
    def fecha_limite(self) -> date: return self._fecha_limite
    @property
    def entregas(self) -> list[EntregaTarea]: return list(self._entregas)



class EntregaTarea:
    def __init__(self, id_entrega: str, archivo_enviado: str, estudiante: Estudiante,
                 tarea: Tarea):
        self._id_entrega = id_entrega
        self._archivo_enviado = archivo_enviado
        self._fecha_entrega: date | None = None
        self._estado_entrega = "PENDIENTE"
        self._nota = 0.0
        self._observaciones = ""
        self._estudiante = estudiante       # realiza: cada entrega pertenece a 1 estudiante
        self._tarea = tarea

    def enviar(self) -> None:
        self._fecha_entrega = date.today()
        tarde = self._fecha_entrega > self._tarea.fecha_limite
        self._estado_entrega = "TARDIA" if tarde else "ENTREGADA"
        self._tarea._registrar_entrega(self)

    def calificar(self, nota: float, observaciones: str = "") -> None:
        if not 0 <= nota <= 20:
            raise ValueError("Nota fuera de rango (0-20)")
        self._nota = nota
        self._observaciones = observaciones
        self._estado_entrega = "CALIFICADA"

    @property
    def id_entrega(self) -> str: return self._id_entrega
    @property
    def archivo_enviado(self) -> str: return self._archivo_enviado
    @property
    def fecha_entrega(self) -> date | None: return self._fecha_entrega
    @property
    def estado_entrega(self) -> str: return self._estado_entrega
    @property
    def nota(self) -> float: return self._nota
    @property
    def observaciones(self) -> str: return self._observaciones
    @property
    def estudiante(self) -> Estudiante: return self._estudiante
