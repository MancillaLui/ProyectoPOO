"""Demostración del flujo de matrícula, tareas y evaluaciones."""
from __future__ import annotations

from datetime import date, timedelta

from .modelos.academico import Curso
from .modelos.preguntas import (
    PreguntaAbierta,
    PreguntaOpcionMultiple,
    PreguntaRespuestaCorta,
    PreguntaVerdaderoFalso,
)
from .modelos.usuarios import Administrador, Docente, Estudiante, Usuario


def main() -> None:
    # Usuarios
    admin = Administrador("ADM01", "Rosa", "Quispe", "rosa@colegio.edu", "admin123", "TOTAL")
    docente = Docente("DOC01", "Luis", "Huamán", "luis@colegio.edu", "doc123", "Matemática")
    ana = Estudiante("EST01", "Ana", "Flores", "ana@colegio.edu", "est123", "3ro", "A")

    registro: list[Usuario] = []
    for u in (admin, docente, ana):
        admin.gestionar_usuarios(registro, u)

    # Curso, unidad y sesión
    curso = Curso("MAT3", "Matemática", "3ro")
    admin.asignar_docente(docente, curso)
    admin.matricular_estudiante(ana, curso)
    unidad = curso.agregar_unidad("U1", "Álgebra")
    sesion = unidad.agregar_sesion("S1", date.today(), "Ecuaciones lineales")

    # Actividades
    docente.publicar_material(sesion, "M1", "Guía de ecuaciones", "PDF", "/materiales/guia.pdf")
    docente.registrar_asistencia(sesion, ana, "PRESENTE")

    tarea = docente.crear_tarea(sesion, "T1", "Ejercicios 1-10", "Resolver",
                                date.today() + timedelta(days=3))
    entrega = ana.entregar_tarea(tarea, "ejercicios_ana.pdf")
    entrega.calificar(18, "Muy buen trabajo")
    print(f"Entrega: {entrega.estado_entrega} | nota {entrega.nota}")

    # Examen con distintos tipos de pregunta
    examen = docente.crear_examen(sesion, "E1", "Examen parcial", 45)
    p1 = PreguntaVerdaderoFalso("P1", "x + 2 = 5 implica x = 3", 2, True)
    p2 = PreguntaOpcionMultiple("P2", "Resuelve 2x = 10", 3, ["3", "5", "10"], "5")
    p3 = PreguntaRespuestaCorta("P3", "Valor de 7 × 6", 5, "42")
    p4 = PreguntaAbierta("P4", "Explica qué es una ecuación", 10, "Claridad y precisión")
    for p in (p1, p2, p3, p4):
        examen.agregar_pregunta(p)

    rendicion = ana.rendir_examen(examen)
    rendicion.responder(p1, "true")
    rendicion.responder(p2, "5")
    rendicion.responder(p3, "42")
    rendicion.responder(p4, "Una igualdad con una incógnita.")

    rendicion.calificar_automatico()        # V/F, múltiple y corta (polimorfismo)
    rendicion.calificar_manual(p4, 8)       # abierta, revisada por el docente
    print(f"Nota final del examen: {rendicion.calcular_nota_final()} / 20")

    print(f"{ana} cursa {ana.ver_cursos()[0].nombre} con {curso.docente}")
