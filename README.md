# Simulador de Editor de Texto con Interfaz Gráfica

Este proyecto implementa un simulador de editor de texto con funcionalidad de deshacer/rehacer (undo/redo) utilizando una estructura Stack propia y una interfaz gráfica creada con tkinter.

## Estructura del Proyecto

- `stack.py`: Implementación de `Stack` (pila) encapsulando una lista de Python.
- `editor.py`: Lógica de negocio (`TextEditor`) con estado, undo/redo y validaciones.
- `main_gui.py`: Interfaz gráfica (tkinter) conectada a `TextEditor`.
- `test_editor.py`: Pruebas unitarias con `unittest` para `Stack` y `TextEditor`.

### Funcionalidades del Editor

- Escribir texto
- Borrar caracteres (especificando cuántos borrar desde el final)
- Deshacer operaciones (undo)
- Rehacer operaciones (redo)
- Historial de todas las acciones realizadas
- Métodos requeridos por el enunciado: `write(text)`, `delete(n)`, `undo()`, `redo()`, `show()`, `history()`

### Validaciones Implementadas

- No se puede escribir texto vacío
- No se puede borrar un número negativo de caracteres
- No se puede borrar más caracteres de los disponibles
- No se puede deshacer cuando no hay acciones para deshacer
- No se puede rehacer cuando no hay acciones para rehacer
- Borrar `0` caracteres no modifica el contenido (no-op)

## Diseño

La aplicación sigue una arquitectura de separación de responsabilidades:

1. Capa de Datos (`stack.py`): Implementa la estructura de datos pila
2. Capa de Lógica de Negocio (`editor.py`): Gestiona el estado del editor y las operaciones
3. Capa de Presentación (`main_gui.py`): Interfaz gráfica de usuario

El patrón de pila se utiliza para implementar las funcionalidades de deshacer/rehacer:

- Cada acción se guarda en la pila de deshacer
- Al deshacer, la acción se mueve de la pila de deshacer a la pila de rehacer
- Al rehacer, la acción se mueve de la pila de rehacer a la pila de deshacer
- Al realizar una nueva acción, la pila de rehacer se vacía


Desarrollado como ejercicio académico.
