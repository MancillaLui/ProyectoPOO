"""Ventanas y formularios conectados con los modelos del proyecto."""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.font import nametofont

from ..modelos.academico import Curso
from ..modelos.preguntas import PreguntaAbierta, PreguntaRespuestaCorta, PreguntaVerdaderoFalso
from ..modelos.usuarios import Administrador, Docente, Estudiante


class Aplicacion(tk.Tk):
    """Coordina la navegación y las operaciones de gestión académica."""

    def __init__(self):
        super().__init__()
        self.title("Aula · Gestión académica")
        self.geometry("1180x780")
        self.minsize(980, 700)
        self.configure(bg="#f4f6fa")
        self.admin = Administrador("ADM01", "Rosa", "Quispe", "rosa@colegio.edu", "admin123", "TOTAL")
        self.docente = Docente("DOC01", "Luis", "Huamán", "luis@colegio.edu", "doc123", "Matemática")
        self.usuarios = [self.admin, self.docente]
        self.cursos = []
        self._revisadas = {}
        self.vista = "Resumen"
        self._estilos()
        self._crear_curso("MAT3", "Matemática", "3ro", "Álgebra", "Ecuaciones lineales")
        ana = Estudiante("EST01", "Ana", "Flores", "ana@colegio.edu", "est123", "3ro", "A")
        self.admin.gestionar_usuarios(self.usuarios, ana)
        self.admin.matricular_estudiante(ana, self.curso)
        self.docente.registrar_asistencia(self.sesion, ana, "PRESENTE")
        tarea = self.docente.crear_tarea(self.sesion, "T1", "Ejercicios de ecuaciones", "Resolver los ejercicios 1 al 10", date.today() + timedelta(days=3))
        ana.entregar_tarea(tarea, "ejercicios_ana.pdf").calificar(18, "Muy buen trabajo")
        self._estructura()
        self.mostrar("Resumen")

    @property
    def sesion(self):
        return self.curso.unidades[0].sesiones[0]

    def _estilos(self):
        nametofont("TkDefaultFont").configure(family="Segoe UI", size=10)
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#f4f6fa")
        style.configure("TLabel", background="#f4f6fa", foreground="#25324b")
        style.configure("Title.TLabel", font=("Segoe UI", 25, "bold"))
        style.configure("Muted.TLabel", foreground="#65748b")
        style.configure("TButton", padding=(14, 9), background="#ffffff", foreground="#25324b")
        style.configure("Primary.TButton", background="#2859d8", foreground="white")
        style.map("Primary.TButton", background=[("active", "#2048b3")])
        style.configure("Treeview", rowheight=36, background="white", fieldbackground="white", borderwidth=0)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), padding=10, background="#e9edf5")
        style.map("Treeview", background=[("selected", "#dbe7ff")], foreground=[("selected", "#16346b")])

    def _crear_curso(self, codigo, nombre, grado, unidad, tema):
        if any(c.id_curso == codigo for c in self.cursos):
            raise ValueError("Ya existe un curso con ese código.")
        curso = Curso(codigo, nombre, grado)
        self.admin.asignar_docente(self.docente, curso)
        sesion = curso.agregar_unidad("U1", unidad).agregar_sesion("S1", date.today(), tema)
        examen = self.docente.crear_examen(sesion, "E1", "Evaluación de práctica", 30)
        examen.agregar_pregunta(PreguntaVerdaderoFalso("P1", "Python permite utilizar clases y objetos.", 5, True))
        examen.agregar_pregunta(PreguntaRespuestaCorta("P2", "¿Qué palabra se usa para definir una clase en Python?", 5, "class"))
        examen.agregar_pregunta(PreguntaAbierta("P3", "Explica con tus palabras qué es la herencia.", 10, "Claridad y uso de un ejemplo"))
        self.cursos.append(curso)
        self.curso = curso

    def _estructura(self):
        sidebar = tk.Frame(self, bg="#14233e", width=205)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="aula", font=("Segoe UI", 32, "bold"), fg="white", bg="#14233e").pack(anchor="w", padx=24, pady=(30, 0))
        tk.Label(sidebar, text="Gestión académica", fg="#aebed8", bg="#14233e").pack(anchor="w", padx=26, pady=(0, 35))
        self.botones = {}
        for vista in ("Resumen", "Estudiantes", "Tareas", "Evaluaciones"):
            button = tk.Button(sidebar, text=vista, anchor="w", relief="flat", bd=0, padx=22, pady=13,
                               bg="#14233e", fg="#c4d0e3", activebackground="#2a4267", activeforeground="white",
                               cursor="hand2", command=lambda nombre=vista: self.mostrar(nombre))
            button.pack(fill="x", padx=12, pady=3)
            self.botones[vista] = button
        tk.Label(sidebar, text="Sesión de demostración\nDatos guardados en memoria", justify="left", fg="#aebed8", bg="#14233e", font=("Segoe UI", 9)).pack(side="bottom", anchor="w", padx=22, pady=25)
        main = ttk.Frame(self, padding=(30, 24))
        main.pack(side="left", fill="both", expand=True)
        header = ttk.Frame(main)
        header.pack(fill="x", pady=(0, 18))
        ttk.Label(header, text="CURSO ACTIVO", style="Muted.TLabel").pack(side="left", padx=(0, 12))
        self.selector = ttk.Combobox(header, state="readonly", width=28)
        self.selector.pack(side="left")
        self.selector.bind("<<ComboboxSelected>>", self._cambiar_curso)
        ttk.Button(header, text="+ Nuevo curso", command=self.nuevo_curso).pack(side="right")
        self.contenido = ttk.Frame(main)
        self.contenido.pack(fill="both", expand=True)
        ttk.Label(main, text="Los cambios se conservan mientras esta ventana esté abierta.", style="Muted.TLabel").pack(anchor="w", pady=(16, 0))

    def _cambiar_curso(self, _event):
        self.curso = self.cursos[self.selector.current()]
        self.mostrar(self.vista)

    def mostrar(self, vista):
        self.vista = vista
        self.selector.configure(values=[f"{c.nombre} · {c.grado} ({c.id_curso})" for c in self.cursos])
        self.selector.current(self.cursos.index(self.curso))
        for nombre, boton in self.botones.items():
            boton.configure(bg="#2a4267" if nombre == vista else "#14233e", fg="white" if nombre == vista else "#c4d0e3")
        for child in self.contenido.winfo_children():
            child.destroy()
        ttk.Label(self.contenido, text=vista, style="Title.TLabel").pack(anchor="w")
        ttk.Label(self.contenido, text=f"{self.curso.nombre} · {self.sesion.tema}", style="Muted.TLabel").pack(anchor="w", pady=(4, 20))
        vistas = {"Resumen": self.resumen, "Estudiantes": self.estudiantes, "Tareas": self.tareas, "Evaluaciones": self.evaluaciones}
        vistas[vista]()

    def _tabla(self, parent, columnas, filas):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, pady=(12, 0))
        table = ttk.Treeview(frame, columns=[str(i) for i in range(len(columnas))], show="headings", selectmode="browse", height=5)
        for i, label in enumerate(columnas):
            table.heading(str(i), text=label)
            table.column(str(i), width=130, minwidth=70)
        for i, row in enumerate(filas):
            table.insert("", "end", iid=str(i), values=row)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scroll.set)
        table.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        if filas:
            table.selection_set("0")
        return table

    def _seleccion(self, tabla, elementos, mensaje):
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona un registro", mensaje, parent=self)
            return None
        return elementos[int(seleccion[0])]

    def _formulario(self, titulo, campos, guardar):
        dialogo = tk.Toplevel(self)
        dialogo.title(titulo)
        dialogo.transient(self)
        dialogo.resizable(False, False)
        frame = ttk.Frame(dialogo, padding=24)
        frame.pack(fill="both", expand=True)
        entradas = {}
        for label, valor in campos:
            ttk.Label(frame, text=label, wraplength=440).pack(anchor="w", pady=(8, 4))
            variable = tk.StringVar(value=valor)
            ttk.Entry(frame, textvariable=variable, width=58, show="*" if label == "Contraseña" else "").pack(fill="x")
            entradas[label] = variable
        error = ttk.Label(frame, text="", foreground="#b42318", wraplength=440)
        error.pack(anchor="w", pady=8)

        def confirmar():
            valores = {label: variable.get().strip() for label, variable in entradas.items()}
            try:
                if not all(valores.values()):
                    raise ValueError("Completa todos los campos.")
                guardar(valores)
            except ValueError as exc:
                error.configure(text=str(exc))
                return
            dialogo.destroy()
            self.mostrar(self.vista)

        ttk.Button(frame, text="Guardar", style="Primary.TButton", command=confirmar).pack(side="right")
        ttk.Button(frame, text="Cancelar", command=dialogo.destroy).pack(side="right", padx=8)
        dialogo.update_idletasks()
        dialogo.geometry(f"+{self.winfo_rootx() + 260}+{self.winfo_rooty() + 70}")
        dialogo.grab_set()

    def nuevo_curso(self):
        def guardar(v):
            self._crear_curso(v["Código"], v["Nombre"], v["Grado"], v["Unidad temática"], v["Tema de la sesión"])
        self._formulario("Nuevo curso", [("Código", ""), ("Nombre", ""), ("Grado", ""), ("Unidad temática", ""), ("Tema de la sesión", "")], guardar)

    def resumen(self):
        cards = ttk.Frame(self.contenido)
        cards.pack(fill="x", pady=(0, 24))
        for label, value in (("Estudiantes", len(self.curso.estudiantes)), ("Tareas", len(self.sesion.tareas)), ("Evaluaciones", len(self.sesion.examenes))):
            card = tk.Frame(cards, bg="white", padx=22, pady=18, highlightbackground="#e2e7ef", highlightthickness=1)
            card.pack(side="left", fill="x", expand=True, padx=(0, 12))
            tk.Label(card, text=str(value), font=("Segoe UI", 30, "bold"), bg="white", fg="#2859d8").pack(anchor="w")
            tk.Label(card, text=label, bg="white", fg="#65748b").pack(anchor="w")
        ttk.Label(self.contenido, text="Tu curso", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 12))
        for texto in (f"Docente   {self.curso.docente}", f"Unidad   {self.curso.unidades[0].titulo}", f"Sesión   {self.sesion.tema}", f"Fecha   {self.sesion.fecha:%d/%m/%Y}"):
            ttk.Label(self.contenido, text=texto).pack(anchor="w", pady=6)
        ttk.Button(self.contenido, text="Ver estudiantes", style="Primary.TButton", command=lambda: self.mostrar("Estudiantes")).pack(anchor="w", pady=20)

    def estudiantes(self):
        barra = ttk.Frame(self.contenido)
        barra.pack(fill="x")
        ttk.Button(barra, text="+ Matricular estudiante", style="Primary.TButton", command=self.matricular).pack(side="left")
        ttk.Button(barra, text="Registrar asistencia", command=self.registrar_asistencia).pack(side="left", padx=10)
        estados = {a.estudiante.codigo_institucional: a.estado for a in self.sesion.asistencias}
        filas = [(e.codigo_institucional, f"{e.nombre} {e.apellido}", e.grado, e.seccion, estados.get(e.codigo_institucional, "Sin registro")) for e in self.curso.estudiantes]
        self.tabla_estudiantes = self._tabla(self.contenido, ["Código", "Estudiante", "Grado", "Sección", "Asistencia"], filas)

    def matricular(self):
        def guardar(v):
            if "@" not in v["Correo"]:
                raise ValueError("Ingresa un correo válido.")
            estudiante = Estudiante(v["Código"], v["Nombre"], v["Apellido"], v["Correo"], v["Contraseña"], self.curso.grado, v["Sección"])
            self.admin.gestionar_usuarios(self.usuarios, estudiante)
            self.admin.matricular_estudiante(estudiante, self.curso)
        self._formulario("Matricular estudiante", [("Código", ""), ("Nombre", ""), ("Apellido", ""), ("Correo", ""), ("Contraseña", ""), ("Sección", "A")], guardar)

    def registrar_asistencia(self):
        estudiante = self._seleccion(self.tabla_estudiantes, self.curso.estudiantes, "Selecciona un estudiante para registrar su asistencia.")
        if estudiante is None:
            return
        def guardar(v):
            estado = v["Estado"].upper()
            if estado not in ("PRESENTE", "AUSENTE", "TARDANZA"):
                raise ValueError("Usa PRESENTE, AUSENTE o TARDANZA.")
            self.docente.registrar_asistencia(self.sesion, estudiante, estado)
        self._formulario(f"Asistencia de {estudiante.nombre}", [("Estado", "PRESENTE")], guardar)

    def tareas(self):
        barra = ttk.Frame(self.contenido)
        barra.pack(fill="x")
        ttk.Button(barra, text="+ Nueva tarea", style="Primary.TButton", command=self.nueva_tarea).pack(side="left")
        ttk.Button(barra, text="Entregar archivo", command=self.entregar).pack(side="left", padx=10)
        ttk.Button(barra, text="Calificar entrega", command=self.calificar_entrega).pack(side="left")
        self.tabla_tareas = self._tabla(self.contenido, ["Tarea", "Descripción", "Fecha límite", "Entregas"], [(t.titulo, t.descripcion, t.fecha_limite.isoformat(), len(t.entregas)) for t in self.sesion.tareas])
        ttk.Label(self.contenido, text="Entregas del curso", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(18, 0))
        self.entregas = [entrega for tarea in self.sesion.tareas for entrega in tarea.entregas]
        self.tabla_entregas = self._tabla(self.contenido, ["Estudiante", "Archivo", "Estado", "Nota"], [(str(e.estudiante), Path(e.archivo_enviado).name, e.estado_entrega, e.nota) for e in self.entregas])

    def nueva_tarea(self):
        def guardar(v):
            try:
                limite = date.fromisoformat(v["Fecha límite (AAAA-MM-DD)"])
            except ValueError:
                raise ValueError("Ingresa una fecha válida con formato AAAA-MM-DD.") from None
            self.docente.crear_tarea(self.sesion, f"T{len(self.sesion.tareas) + 1}", v["Título"], v["Descripción"], limite)
        self._formulario("Nueva tarea", [("Título", ""), ("Descripción", ""), ("Fecha límite (AAAA-MM-DD)", (date.today() + timedelta(days=3)).isoformat())], guardar)

    def entregar(self):
        tarea = self._seleccion(self.tabla_tareas, self.sesion.tareas, "Selecciona una tarea para entregar.")
        if tarea is None:
            return
        if not self.curso.estudiantes:
            messagebox.showinfo("Matrícula requerida", "Primero matricula un estudiante en este curso.", parent=self)
            return
        archivo = filedialog.askopenfilename(title="Selecciona el archivo de la tarea", parent=self)
        if not archivo:
            return
        def guardar(v):
            estudiantes = {e.codigo_institucional: e for e in self.curso.estudiantes}
            if v["Código del estudiante"] not in estudiantes:
                raise ValueError("El estudiante debe estar matriculado en el curso activo.")
            estudiantes[v["Código del estudiante"]].entregar_tarea(tarea, archivo)
        self._formulario("Entregar tarea", [("Código del estudiante", self.curso.estudiantes[0].codigo_institucional)], guardar)

    def calificar_entrega(self):
        entrega = self._seleccion(self.tabla_entregas, self.entregas, "Selecciona una entrega para calificar.")
        if entrega is None:
            return
        def guardar(v):
            entrega.calificar(float(v["Nota (0 a 20)"]), v["Observaciones"])
        self._formulario("Calificar entrega", [("Nota (0 a 20)", str(entrega.nota)), ("Observaciones", entrega.observaciones or "Revisado")], guardar)

    def evaluaciones(self):
        examen = self.sesion.examenes[0]
        ttk.Label(self.contenido, text=f"{examen.titulo} · {examen.duracion_minutos} minutos · 20 puntos", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        ttk.Label(self.contenido, text="Práctica sobre POO. Las preguntas abiertas se revisan manualmente.", style="Muted.TLabel").pack(anchor="w", pady=(6, 14))
        barra = ttk.Frame(self.contenido)
        barra.pack(fill="x")
        ttk.Button(barra, text="Responder examen", style="Primary.TButton", command=self.responder_examen).pack(side="left")
        ttk.Button(barra, text="Revisar pregunta abierta", command=self.revisar_examen).pack(side="left", padx=10)
        filas = []
        for rendicion in examen.rendiciones:
            estado = "Pendiente de revisión"
            if rendicion.id_rendicion in self.revisadas:
                estado = "Revisado"
            filas.append((str(rendicion.estudiante), rendicion.calcular_nota_final(), estado))
        self.tabla_examenes = self._tabla(self.contenido, ["Estudiante", "Puntaje / 20", "Revisión manual"], filas)

    @property
    def revisadas(self):
        return self._revisadas.setdefault(self.curso.id_curso, set())

    def responder_examen(self):
        if not self.curso.estudiantes:
            messagebox.showinfo("Matrícula requerida", "Primero matricula un estudiante en este curso.", parent=self)
            return
        examen = self.sesion.examenes[0]
        campos = [("Código del estudiante", self.curso.estudiantes[0].codigo_institucional)]
        campos.extend((p.enunciado, "") for p in examen.preguntas)
        def guardar(v):
            estudiantes = {e.codigo_institucional: e for e in self.curso.estudiantes}
            if v["Código del estudiante"] not in estudiantes:
                raise ValueError("El estudiante debe estar matriculado en el curso activo.")
            if v[examen.preguntas[0].enunciado].lower() not in ("true", "verdadero", "v", "false", "falso", "f"):
                raise ValueError("En la primera pregunta, escribe verdadero o falso.")
            rendicion = estudiantes[v["Código del estudiante"]].rendir_examen(examen)
            for pregunta in examen.preguntas:
                rendicion.responder(pregunta, v[pregunta.enunciado])
            rendicion.calificar_automatico()
            rendicion.calcular_nota_final()
        self._formulario("Responder examen", campos, guardar)

    def revisar_examen(self):
        rendicion = self._seleccion(self.tabla_examenes, self.sesion.examenes[0].rendiciones, "Selecciona un examen respondido para revisarlo.")
        if rendicion is None:
            return
        respuesta = rendicion.respuestas[-1]
        dialogo = tk.Toplevel(self)
        dialogo.title("Respuesta abierta")
        dialogo.transient(self)
        frame = ttk.Frame(dialogo, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text=respuesta.pregunta.enunciado, wraplength=500).pack(anchor="w")
        texto = tk.Text(frame, width=64, height=8, wrap="word")
        texto.insert("1.0", respuesta.respuesta_texto)
        texto.configure(state="disabled")
        texto.pack(pady=15)
        ttk.Label(frame, text=f"Criterio de evaluación · {respuesta.pregunta.criterio_evaluacion}", wraplength=500).pack(anchor="w")
        def calificar():
            dialogo.destroy()
            def guardar(v):
                rendicion.calificar_manual(respuesta.pregunta, float(v["Puntaje (0 a 10)"]))
                rendicion.calcular_nota_final()
                self.revisadas.add(rendicion.id_rendicion)
            self._formulario("Calificar respuesta abierta", [("Puntaje (0 a 10)", str(respuesta.puntaje_obtenido))], guardar)
        ttk.Button(frame, text="Asignar puntaje", style="Primary.TButton", command=calificar).pack(anchor="e", pady=(16, 0))
        dialogo.grab_set()


def main():
    Aplicacion().mainloop()
