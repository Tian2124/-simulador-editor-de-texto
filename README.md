# Simulador de Editor de Texto con Interfaz Gráfica

Este proyecto implementa un simulador de editor de texto con funcionalidad de deshacer/rehacer (undo/redo) utilizando una **estructura Stack propia** y una interfaz gráfica creada con **tkinter**.

## Estructura del Proyecto

- `stack.py`: Implementación de `Stack` (pila) encapsulando una lista de Python.
- `editor.py`: Lógica de negocio (`TextEditor`) con estado, undo/redo y validaciones.
- `main_gui.py`: Interfaz gráfica (tkinter) conectada a `TextEditor`.
- `test_editor.py`: Pruebas unitarias con `unittest` para `Stack` y `TextEditor`.

## Requisitos

- Python 3.12+
- Sin base de datos
- Sin frameworks web
- Sin librerías externas de estructuras de datos

## Preparación del entorno (primera vez)

### 1) Instalar Python (si no está instalado)

Estas instrucciones están pensadas para alguien que nunca instaló Python.

#### Opción A (recomendada): Sitio oficial

- Abre el navegador y busca: **Python 3.12 download**
- Entra a `python.org` → **Downloads** → descarga **Python 3.12.x**
- Ejecuta el instalador y **marca** la casilla **“Add python.exe to PATH”**
- Clic en **Install Now** y finaliza

Verifica la instalación en una terminal (PowerShell o CMD):

```bash
python --version
```

Si `python` no se reconoce, prueba:

```bash
py --version
```

#### Opción B (más simple): Microsoft Store (Windows)

- Abre **Microsoft Store**
- Busca **Python 3.12**
- Instala y luego verifica con:

```bash
python --version
```

### 2) (Opcional) Crear y activar un entorno virtual

En Windows (PowerShell):

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Dependencias

Este proyecto usa **solo librerías estándar** (incluye `tkinter` y `unittest`).

- En **Windows** normalmente `tkinter` ya viene con Python.
- En **Linux**, si al ejecutar la GUI aparece error de `tkinter`, instala el paquete de Tk de tu distro (por ejemplo, en Debian/Ubuntu suele ser `python3-tk`).

## Ejecución

Para ejecutar la aplicación principal:

```bash
python main_gui.py
```

Para ejecutar las pruebas unitarias:

```bash
python -m unittest -v
```

## Características

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

1. **Capa de Datos** (`stack.py`): Implementa la estructura de datos pila
2. **Capa de Lógica de Negocio** (`editor.py`): Gestiona el estado del editor y las operaciones
3. **Capa de Presentación** (`main_gui.py`): Interfaz gráfica de usuario

El patrón de pila se utiliza para implementar las funcionalidades de deshacer/rehacer:

- Cada acción se guarda en la pila de deshacer
- Al deshacer, la acción se mueve de la pila de deshacer a la pila de rehacer
- Al rehacer, la acción se mueve de la pila de rehacer a la pila de deshacer
- Al realizar una nueva acción, la pila de rehacer se vacía

## Entregables (según la tarea)

Este repositorio incluye **código fuente**, **README** y **pruebas mínimas**. Además, para la entrega final normalmente se solicita:

- PDF con descripción, explicación LIFO, capturas, validaciones, y links
- Video en Google Drive (máx 3 minutos) con permisos de lectura
- Link a repositorio público (GitHub)

## Autores

Desarrollado como ejercicio académico.
