"""Tipos de pregunta y sus reglas de evaluación."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Pregunta(ABC):
    def __init__(self, id_pregunta: str, enunciado: str, puntaje: float):
        self._id_pregunta = id_pregunta
        self._enunciado = enunciado
        self._puntaje = puntaje

    @abstractmethod
    def evaluar(self, respuesta: str) -> float:
        """Devuelve el puntaje obtenido (0 .. puntaje) para la respuesta dada."""

    def requiere_revision_manual(self) -> bool:
        return False

    @property
    def id_pregunta(self) -> str: return self._id_pregunta
    @property
    def enunciado(self) -> str: return self._enunciado
    @property
    def puntaje(self) -> float: return self._puntaje



class PreguntaVerdaderoFalso(Pregunta):
    def __init__(self, id_pregunta, enunciado, puntaje, respuesta_correcta: bool):
        super().__init__(id_pregunta, enunciado, puntaje)
        self._respuesta_correcta = respuesta_correcta

    def evaluar(self, respuesta: str) -> float:
        valor = respuesta.strip().lower() in ("true", "verdadero", "v")
        return self._puntaje if valor == self._respuesta_correcta else 0.0



class PreguntaRespuestaCorta(Pregunta):
    def __init__(self, id_pregunta, enunciado, puntaje, respuesta_correcta: str):
        super().__init__(id_pregunta, enunciado, puntaje)
        self._respuesta_correcta = respuesta_correcta

    def evaluar(self, respuesta: str) -> float:
        coincide = respuesta.strip().lower() == self._respuesta_correcta.lower()
        return self._puntaje if coincide else 0.0



class PreguntaAbierta(Pregunta):
    def __init__(self, id_pregunta, enunciado, puntaje, criterio_evaluacion: str):
        super().__init__(id_pregunta, enunciado, puntaje)
        self._criterio_evaluacion = criterio_evaluacion

    def evaluar(self, respuesta: str) -> float:
        return 0.0                           # pendiente de revisión del docente

    def requiere_revision_manual(self) -> bool:
        return True

    @property
    def criterio_evaluacion(self) -> str: return self._criterio_evaluacion



class PreguntaOpcionMultiple(Pregunta):
    def __init__(self, id_pregunta, enunciado, puntaje, opciones: list[str],
                 respuesta_correcta: str):
        super().__init__(id_pregunta, enunciado, puntaje)
        self._opciones = list(opciones)
        self._respuesta_correcta = respuesta_correcta

    def evaluar(self, respuesta: str) -> float:
        return self._puntaje if respuesta.strip() == self._respuesta_correcta else 0.0

    @property
    def opciones(self) -> list[str]: return list(self._opciones)
