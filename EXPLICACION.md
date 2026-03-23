# Explicación del proyecto

Este documento explica qué hace cada archivo, cómo funciona la lógica de undo/redo con Stack (LIFO) y por qué se diseñó así (separación UI/Lógica/Datos) 


## 1) ¿Qué hace el programa?

El programa simula un editor de texto muy simple con:

- Escritura (agregar texto al final)
- Borrado (eliminar los últimos `n` caracteres)
- Deshacer (undo) y rehacer (redo) usando pilas (Stack) con comportamiento LIFO
- Historial (log) de acciones y validaciones

La interfaz es gráfica usando tkinter.

---

## 2) Estructura y explicación por archivo

### `stack.py` (Estructura de datos)

#### `stack.py`: Qué hace

- Define la clase `Stack`, que encapsula una lista de Python (`self._items`) para modelar una pila.

#### `stack.py`: Cómo lo hace

- `push(item)`: agrega al final de la lista (top de la pila).
- `pop()`: saca y retorna el último elemento; si está vacía, lanza `IndexError`.
- `peek()`: retorna el último elemento sin sacarlo; si está vacía, lanza `IndexError`.
- `is_empty()`: retorna `True` si no hay elementos.
- `size()`: retorna el tamaño.

#### `stack.py`: Por qué se hizo así

- La tarea pide implementar una Stack propia (no usar estructuras externas).
- Usar una lista interna es la forma más simple y directa de implementar LIFO en Python manteniendo la clase encapsulada y reutilizable.

---

### `editor.py` (Lógica de negocio / Estado)

#### `editor.py`: Qué hace

- Implementa `TextEditor` con:
  - `current_text` (estado actual del texto)
  - `undo_stack` (pila de acciones para deshacer)
  - `redo_stack` (pila de acciones para rehacer)
  - `history` (lista de strings descriptivos)

#### `editor.py`: Cómo lo hace (idea central)

- Cada acción del usuario genera una acción inversa que se apila en `undo_stack`.
- Al ejecutar `undo()`, se aplica esa acción inversa y se guarda la acción complementaria en `redo_stack`.
- Al ejecutar `redo()`, se aplica lo que estaba en `redo_stack` y se guarda el complemento en `undo_stack`.
- Cuando se hace una acción nueva (`write` o `delete`), se limpia `redo_stack` (porque ya no tiene sentido rehacer acciones de un “futuro” que cambió).

#### `editor.py`: Representación interna de acciones

- Se guardan tuplas `(tipo, dato)`:
  - `("delete", n)` significa: “para revertir, borrar `n` caracteres al final”.
  - `("insert", texto)` significa: “para revertir, insertar este `texto` al final”.

#### `editor.py`: Métodos principales

- `write(text)`:
  - Valida que `text` no esté vacío.
  - Agrega texto al final.
  - Guarda en `undo_stack` la inversa: `("delete", len(text))`.
  - Limpia `redo_stack`.
  - Agrega registro al `history`.

- `delete(n)`:
  - Valida `n >= 0` y `n <= len(current_text)`.
  - Caso especial: `n == 0` → no-op (no modifica el texto).
  - Recorta los últimos `n` caracteres.
  - Guarda en `undo_stack` la inversa: `("insert", deleted_text)`.
  - Limpia `redo_stack`.
  - Registra en `history`.

- `undo()`:
  - Si `undo_stack` está vacía, lanza `IndexError`.
  - Saca una acción del undo y la aplica.
  - Guarda en `redo_stack` la acción complementaria (para poder rehacer).
  - Registra en `history`.

- `redo()`:
  - Si `redo_stack` está vacía, lanza `IndexError`.
  - Saca una acción del redo y la aplica.
  - Guarda en `undo_stack` la acción complementaria (para poder deshacer lo rehecho).
  - Registra en `history`.

- `show()` y `history()`:
  - Son alias requeridos por el enunciado para mostrar contenido e historial.
  - Internamente delegan a `get_content()` y `get_history()`.

#### `editor.py`: Por qué se hizo así

- Se cumple la separación de responsabilidades: `TextEditor` no sabe nada de tkinter, solo maneja lógica y datos.
- `undo/redo` queda claramente basado en LIFO:
  - “lo último que hice” es lo primero que se deshace.
- Guardar acciones inversas simplifica el modelo y evita almacenar snapshots completos del texto en cada paso.

---

### `main_gui.py` (Interfaz gráfica)

#### `main_gui.py`: Qué hace

- Construye la ventana y los controles:
  - Área no editable con el texto actual
  - Entrada para escribir + botón Escribir
  - Entrada numérica para borrar + botón Borrar
  - Botones Deshacer y Rehacer
  - Área de historial (log)

#### `main_gui.py`: Cómo lo hace

- Instancia un `TextEditor` y cada botón llama a un método:
  - `Escribir` → `editor.write(...)`
  - `Borrar` → `editor.delete(...)`
  - `Deshacer` → `editor.undo()`
  - `Rehacer` → `editor.redo()`
- Maneja errores con `messagebox.showerror`:
  - escribir vacío
  - borrar inválido (no entero, negativo o mayor al texto)
  - undo/redo cuando no hay acciones

#### `main_gui.py`: Por qué se hizo así

- La UI solo coordina interacción: captura inputs, llama lógica, muestra resultados.
- Cualquier cambio en reglas/validaciones se hace en `editor.py` sin tocar la UI.

---

### `test_editor.py` (Pruebas unitarias)

#### `test_editor.py`: Qué hace

- Prueba `Stack` (LIFO, tamaño, peek/pop, errores por vacío).
- Prueba `TextEditor` (write/delete/undo/redo + validaciones y casos límite).

#### `test_editor.py`: Cómo lo hace

- Usa `unittest` y aserciones.
- Verifica que el contenido y el historial se actualicen y que las excepciones salten cuando corresponde.

---

## 3) Validaciones implementadas (lo que debes demostrar)

- `write("")` → error (texto vacío).
- `delete(n)`:
  - `n < 0` → error.
  - `n > len(texto)` → error.
  - `n == 0` → no-op (no cambia el texto).
- `undo()` sin acciones → error.
- `redo()` sin acciones → error.
---
