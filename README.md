# Sistema de gestión académica

Proyecto de programación orientada a objetos (POO) en Python que implementa un modelo de gestión académica basado en un diagrama de clases UML. La demostración sigue a una estudiante desde su matrícula en un curso hasta la entrega de una tarea y la calificación de un examen.

## Funcionalidades

- **Usuarios y matrícula.** El administrador registra usuarios, asigna docentes a cursos y matricula estudiantes.
- **Organización de los cursos.** Cada curso se divide en unidades temáticas, que a su vez contienen sesiones de clase.
- **Actividades por sesión.** El docente registra asistencia, publica referencias a materiales didácticos y crea tareas y exámenes.
- **Entregas y calificaciones.** El sistema compara la fecha de entrega con la fecha límite para marcar entregas tardías. Las tareas se califican de 0 a 20 y pueden incluir observaciones.
- **Evaluación de exámenes.** Las preguntas de verdadero o falso, opción múltiple y respuesta corta se califican automáticamente. Las preguntas abiertas se califican de forma manual. La nota del examen es la suma de los puntajes obtenidos.

## Ejecutar la aplicación

Usa Python 3.10 o posterior con Tkinter, incluido en el instalador habitual de Python para Windows. El proyecto solo utiliza la biblioteca estándar de Python.

```bash
git clone https://github.com/MancillaLui/ProyectoPOO.git
cd ProyectoPOO
python sistema_educativo.py
```

También puedes ejecutar el paquete desde la raíz del proyecto.

```bash
python -m gestion_academica
```

Se abrirá una ventana con navegación por resumen, estudiantes, tareas y evaluaciones. Puedes crear cursos, matricular estudiantes, registrar asistencia, crear y entregar tareas, calificarlas y responder un examen de práctica sobre POO. Cada curso nuevo incluye una unidad, una sesión y ese examen de práctica. El docente de ejemplo se asigna a los cursos creados.

El sistema inicia con datos de ejemplo de Matemática. Los cambios se mantienen en memoria durante la ejecución y se pierden al cerrar la ventana. Los archivos entregados se registran mediante su ruta local.

## Demostración en consola

Para ejecutar el ejemplo original en la terminal, agrega `--demo` a cualquiera de los dos comandos.

```bash
python sistema_educativo.py --demo
python -m gestion_academica --demo
```

Esta es la salida esperada.

```text
Entrega: CALIFICADA | nota 18
Nota final del examen: 18 / 20
Ana Flores (EST01) cursa Matemática con Luis Huamán (DOC01)
```

## Estructura del proyecto

```text
ProyectoPOO/
├── .gitignore
├── README.md
├── sistema_educativo.py
└── gestion_academica/
    ├── __init__.py
    ├── __main__.py
    ├── demo.py
    ├── interfaz/
    │   ├── __init__.py
    │   └── aplicacion.py
    └── modelos/
        ├── __init__.py
        ├── usuarios.py
        ├── academico.py
        ├── actividades.py
        ├── preguntas.py
        └── evaluaciones.py
```

| Archivo | Responsabilidad |
| --- | --- |
| `sistema_educativo.py` | Inicia la aplicación y permite seguir importando las clases desde el módulo original. |
| `gestion_academica/__main__.py` | Selecciona la interfaz gráfica o la demostración de consola con `--demo`. |
| `gestion_academica/interfaz/aplicacion.py` | Contiene la ventana, los formularios y su conexión con los modelos. |
| `gestion_academica/demo.py` | Contiene la función `main()` con el recorrido de ejemplo. |
| `gestion_academica/modelos/usuarios.py` | Define `Usuario`, `Administrador`, `Docente` y `Estudiante`. |
| `gestion_academica/modelos/academico.py` | Define `Curso`, `UnidadTematica` y `SesionClase`. |
| `gestion_academica/modelos/actividades.py` | Define `Asistencia`, `MaterialDidactico`, `Tarea` y `EntregaTarea`. |
| `gestion_academica/modelos/preguntas.py` | Define la clase base `Pregunta` y sus cuatro tipos. |
| `gestion_academica/modelos/evaluaciones.py` | Define `Examen`, `RendicionExamen` y `RespuestaEstudiante`. |

Para utilizar las clases en otro archivo, impórtalas desde su módulo correspondiente.

```python
from gestion_academica.modelos.academico import Curso
from gestion_academica.modelos.usuarios import Administrador, Estudiante
```

## Diseño orientado a objetos

| Concepto | Aplicación en el código |
| --- | --- |
| Abstracción y herencia | `Usuario` es la clase base abstracta de `Administrador`, `Docente` y `Estudiante`. `Pregunta` define el método `evaluar()` para los distintos tipos de pregunta. |
| Encapsulamiento | Las clases exponen propiedades de lectura con `@property` y devuelven copias de sus listas para proteger las colecciones internas. |
| Composición | Un `Curso` crea sus objetos `UnidadTematica`, y cada unidad crea sus objetos `SesionClase`. |
| Polimorfismo | `RendicionExamen` llama a `evaluar()` para que cada tipo de pregunta de corrección automática aplique su propia regla. |
