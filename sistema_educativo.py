"""Sistema de gestión académica: implementación del diagrama de clases UML.

Convenciones:
- Atributos privados -> prefijo "_" y acceso de lectura mediante @property.
- Clases abstractas (Usuario, Pregunta) -> abc.ABC.
- Dates del diagrama -> datetime.date / datetime.datetime.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta
from pathlib import Path


# ============================================================
# 2.1 MÓDULO DE USUARIOS
# ============================================================

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


# ============================================================
# 2.2 MÓDULO ACADÉMICO Y ESTRUCTURA DEL CURSO
# ============================================================

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


# ============================================================
# 2.3 MÓDULO DE ACTIVIDADES Y RECURSOS
# ============================================================

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


# ============================================================
# 2.5 MÓDULO DE PREGUNTAS (ABSTRACCIÓN + HERENCIA + POLIMORFISMO)
# (definido antes que las evaluaciones por legibilidad)
# ============================================================

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


# ============================================================
# 2.4 MÓDULO DE EVALUACIONES
# ============================================================

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


# ============================================================
# DEMO
# ============================================================

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


if __name__ == "__main__":
    main()
