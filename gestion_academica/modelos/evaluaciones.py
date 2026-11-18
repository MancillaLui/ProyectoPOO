"""Exámenes, respuestas y calificaciones de cada rendición."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from .preguntas import Pregunta

if TYPE_CHECKING:
    from .usuarios import Estudiante


class Examen:
    def __init__(self, id_examen: str, titulo: str, duracion_minutos: int):
        self._id_examen = id_examen
        self._titulo = titulo
        self._duracion_minutos = duracion_minutos
        self._preguntas: list[Pregunta] = []                # contiene 1..*
        self._rendiciones: list[RendicionExamen] = []       # genera 0..*

    def agregar_pregunta(self, pregunta: Pregunta) -> None:
        self._preguntas.append(pregunta)

    def _registrar_rendicion(self, rendicion: RendicionExamen) -> None:
        self._rendiciones.append(rendicion)

    @property
    def id_examen(self) -> str: return self._id_examen
    @property
    def titulo(self) -> str: return self._titulo
    @property
    def duracion_minutos(self) -> int: return self._duracion_minutos
    @property
    def preguntas(self) -> list[Pregunta]: return list(self._preguntas)
    @property
    def rendiciones(self) -> list[RendicionExamen]: return list(self._rendiciones)



class RespuestaEstudiante:
    def __init__(self, pregunta: Pregunta, respuesta_texto: str):
        self._pregunta = pregunta                # responde a 1 Pregunta
        self._respuesta_texto = respuesta_texto
        self._puntaje_obtenido = 0.0

    def _set_puntaje(self, puntaje: float) -> None:
        self._puntaje_obtenido = puntaje

    @property
    def pregunta(self) -> Pregunta: return self._pregunta
    @property
    def respuesta_texto(self) -> str: return self._respuesta_texto
    @property
    def puntaje_obtenido(self) -> float: return self._puntaje_obtenido



class RendicionExamen:
    def __init__(self, id_rendicion: str, estudiante: Estudiante, examen: Examen):
        self._id_rendicion = id_rendicion
        self._fecha_inicio = datetime.now()
        self._fecha_fin: datetime | None = None
        self._nota_final = 0.0
        self._estudiante = estudiante                       # rinde: 1
        self._examen = examen
        self._respuestas: list[RespuestaEstudiante] = []    # composición 1..*

    def responder(self, pregunta: Pregunta, respuesta_texto: str) -> None:
        if pregunta not in self._examen.preguntas:
            raise ValueError("La pregunta no pertenece a este examen")
        self._respuestas.append(RespuestaEstudiante(pregunta, respuesta_texto))

    def calificar_automatico(self) -> None:
        """Polimorfismo: cada subclase de Pregunta decide cómo validar la respuesta."""
        if self._fecha_fin is None:
            self._fecha_fin = datetime.now()
        for r in self._respuestas:
            if not r.pregunta.requiere_revision_manual():
                r._set_puntaje(r.pregunta.evaluar(r.respuesta_texto))

    def calificar_manual(self, pregunta: Pregunta, puntaje: float) -> None:
        for r in self._respuestas:
            if r.pregunta is pregunta:
                if not 0 <= puntaje <= pregunta.puntaje:
                    raise ValueError("Puntaje fuera de rango")
                r._set_puntaje(puntaje)
                return
        raise ValueError("No hay respuesta para esa pregunta")

    def calcular_nota_final(self) -> float:
        self._nota_final = sum(r.puntaje_obtenido for r in self._respuestas)
        return self._nota_final

    @property
    def id_rendicion(self) -> str: return self._id_rendicion
    @property
    def fecha_inicio(self) -> datetime: return self._fecha_inicio
    @property
    def fecha_fin(self) -> datetime | None: return self._fecha_fin
    @property
    def nota_final(self) -> float: return self._nota_final
    @property
    def estudiante(self) -> Estudiante: return self._estudiante
    @property
    def respuestas(self) -> list[RespuestaEstudiante]: return list(self._respuestas)
