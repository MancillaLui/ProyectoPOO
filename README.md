# Sistema de gestión académica

Proyecto de programación orientada a objetos (POO) en Python que implementa un modelo de gestión académica basado en un diagrama de clases UML. La demostración sigue a una estudiante desde su matrícula en un curso hasta la entrega de una tarea y la calificación de un examen.

## Funcionalidades

- **Usuarios y matrícula.** El administrador registra usuarios, asigna docentes a cursos y matricula estudiantes.
- **Organización de los cursos.** Cada curso se divide en unidades temáticas, que a su vez contienen sesiones de clase.
- **Actividades por sesión.** El docente registra asistencia, publica referencias a materiales didácticos y crea tareas y exámenes.
- **Entregas y calificaciones.** El sistema compara la fecha de entrega con la fecha límite para marcar entregas tardías. Las tareas se califican de 0 a 20 y pueden incluir observaciones.
- **Evaluación de exámenes.** Las preguntas de verdadero o falso, opción múltiple y respuesta corta se califican automáticamente. Las preguntas abiertas se califican de forma manual. La nota del examen es la suma de los puntajes obtenidos.

## Ejecutar la demostración

Usa Python 3.10 o posterior. El proyecto solo utiliza la biblioteca estándar de Python.

```bash
git clone https://github.com/MancillaLui/ProyectoPOO.git
cd ProyectoPOO
python sistema_educativo.py
```

La demostración se ejecuta en la terminal con datos de ejemplo que se mantienen en memoria durante la ejecución. Esta es la salida esperada.

```text
Entrega: CALIFICADA | nota 18
Nota final del examen: 18 / 20
Ana Flores (EST01) cursa Matemática con Luis Huamán (DOC01)
```

## Diseño orientado a objetos

El modelo y la función `main()` están en [sistema_educativo.py](sistema_educativo.py).

| Concepto | Aplicación en el código |
| --- | --- |
| Abstracción y herencia | `Usuario` es la clase base abstracta de `Administrador`, `Docente` y `Estudiante`. `Pregunta` define el método `evaluar()` para los distintos tipos de pregunta. |
| Encapsulamiento | Las clases exponen propiedades de lectura con `@property` y devuelven copias de sus listas para proteger las colecciones internas. |
| Composición | Un `Curso` crea sus objetos `UnidadTematica`, y cada unidad crea sus objetos `SesionClase`. |
| Polimorfismo | `RendicionExamen` llama a `evaluar()` para que cada tipo de pregunta de corrección automática aplique su propia regla. |
