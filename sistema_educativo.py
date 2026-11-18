"""Punto de entrada y acceso compatible a los modelos del sistema académico."""

from gestion_academica.demo import main
from gestion_academica.modelos.usuarios import (
    Usuario,
    Docente,
    Estudiante,
    Administrador,
)
from gestion_academica.modelos.academico import (
    Curso,
    UnidadTematica,
    SesionClase,
)
from gestion_academica.modelos.actividades import (
    Asistencia,
    MaterialDidactico,
    Tarea,
    EntregaTarea,
)
from gestion_academica.modelos.preguntas import (
    Pregunta,
    PreguntaVerdaderoFalso,
    PreguntaRespuestaCorta,
    PreguntaAbierta,
    PreguntaOpcionMultiple,
)
from gestion_academica.modelos.evaluaciones import (
    Examen,
    RespuestaEstudiante,
    RendicionExamen,
)

__all__ = [
    "main",
    "Usuario",
    "Docente",
    "Estudiante",
    "Administrador",
    "Curso",
    "UnidadTematica",
    "SesionClase",
    "Asistencia",
    "MaterialDidactico",
    "Tarea",
    "EntregaTarea",
    "Pregunta",
    "PreguntaVerdaderoFalso",
    "PreguntaRespuestaCorta",
    "PreguntaAbierta",
    "PreguntaOpcionMultiple",
    "Examen",
    "RespuestaEstudiante",
    "RendicionExamen",
]


if __name__ == "__main__":
    from gestion_academica.__main__ import main as iniciar

    iniciar()
