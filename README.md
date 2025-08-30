

Contenido:
- `src/regex_parser.py`: Shunting Yard + inserción de concatenación
- `src/nfa.py`: Construcción de AFN (Thompson) y serialización
- `src/dfa.py`: Construcción de AFD por subconjuntos y simulación
- `src/minimizer.py`: Minimización de AFD (Hopcroft)
- `src/visualize.py`: Exportar Graphviz
- `examples/run_example.py`: pequeño ejemplo de uso

- --

Estructura principal
- `main.py` — script principal. Lee un archivo con expresiones regulares (por defecto `regexes.txt`) y procesa cada regex creando una carpeta con los resultados.
- `src/` — código fuente:
	- `regex_parser.py` — parser y conversión a postfix (Shunting Yard).
	- `nfa.py` — construcción AFN (Thompson) y export a JSON.
	- `dfa.py` — conversión AFN→AFD, simulador y traza.
	- `minimizer.py` — Hopcroft (minimización).
	- `visualize.py` — export a PNG usando Graphviz (opcional).
- `examples/run_example.py` — ejemplo antiguo de uso.
- `regexes.txt` — archivo de ejemplo con expresiones regulares (una por línea).

Instalación (Linux)
```bash
# Opcional: crear y activar virtualenv (Linux):
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias (graphviz es opcional pero recomendado para PNGs):
pip install -r requirements.txt
```

Uso
- Procesar varias regex desde un archivo (por defecto `regexes.txt`):



- Ejecutar el ejemplo individual:

```bash
python3 examples/run_example.py
```

Salida / formato
- Para cada regex se crea `resultados/<TIMESTAMP>/<SAFE_REGEX>/` con:
	- `nfa.json`, `dfa.json`, `mdfa.json` — autómatas serializados (campos: ESTADOS, SIMBOLOS, INICIO, ACEPTACION, TRANSICIONES).
	- `nfa.png`, `dfa.png`, `mdfa.png` — imágenes (si `graphviz` está instalado).
- En consola se muestran: postfix, resumen del AFN, rutas generadas y traza de simulación (paso a paso).

Detalles de diseño
- Epsilon interno representado como `None` (serializa como `'ε'`).
- La conversión a postfix añade un operador explícito de concatenación `.`.
- `safe_regex` es un nombre de carpeta derivado de la regex con caracteres no alfanuméricos reemplazados por `_` y truncado a 40 chars.

