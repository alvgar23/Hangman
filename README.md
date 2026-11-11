# Hangman — Juego del ahorcado

Proyecto de Python que comenzó en 2020 como un ahorcado para terminal y evolucionó en 2025 hacia una versión bilingüe con información lingüística y una interfaz web con Streamlit.

El repositorio conserva las **tres versiones originales**, sin modificar su lógica.

## Versiones

| Versión | Archivo | Fecha indicada en el código | Características |
| --- | --- | --- | --- |
| v1 | [`versiones/2020/ahorcado_v1.py`](versiones/2020/ahorcado_v1.py) | 7 de diciembre de 2020 | Juego de terminal. Selecciona palabras inglesas de NLTK, intenta traducirlas al español con TextBlob y ofrece seis fallos antes de perder. |
| v2 | [`versiones/2025/ahorcado_v2.py`](versiones/2025/ahorcado_v2.py) | 10 de noviembre de 2025 | Juego de terminal con elección de inglés o español, palabras filtradas por frecuencia, categoría gramatical y categoría semántica. |
| v3 | [`versiones/2025/ahorcado_v3.py`](versiones/2025/ahorcado_v3.py) | 10 de noviembre de 2025 | Interfaz web con Streamlit, estado de partida, dibujo del ahorcado, información lingüística y opción de volver a jugar. |

## Cómo se juega

El programa escoge una palabra y la muestra oculta con guiones. Se introducen letras para descubrirla; cada error consume uno de los seis intentos y añade una parte al dibujo. Se gana al descubrir todas las letras y se pierde al agotar los intentos.

## Requisitos

- Python 3.
- **v1:** `nltk` y `textblob`. También requiere el corpus de palabras de NLTK.
- **v2:** `nltk`, `textblob` y `wordfreq`.
- **v3:** `nltk`, `textblob`, `wordfreq` y `streamlit`.

Para instalar las bibliotecas:

```bash
python -m pip install nltk textblob wordfreq streamlit
```

La primera versión necesita descargar el corpus `words` si aún no está disponible:

```bash
python -c "import nltk; nltk.download('words')"
```

Las versiones 2 y 3 intentan descargar automáticamente algunos recursos de NLTK (`punkt`, `averaged_perceptron_tagger` y `wordnet`). Según la versión instalada de NLTK, pueden requerirse otros paquetes de datos.

## Ejecutar cada versión

Desde la raíz del repositorio:

**v1 — consola original**

```bash
python versiones/2020/ahorcado_v1.py
```

**v2 — consola bilingüe**

```bash
python versiones/2025/ahorcado_v2.py
```

**v3 — aplicación web**

```bash
python -m streamlit run versiones/2025/ahorcado_v3.py
```

La versión web se abre en el navegador mediante el servidor local de Streamlit.

## Qué aportan las versiones de 2025

- Selección de idioma (inglés o español).
- Palabras inglesas seleccionadas mediante `wordfreq`, con una frecuencia mínima.
- Intento de traducción al español mediante `TextBlob`.
- Categoría gramatical (POS) mediante NLTK.
- Categoría semántica aproximada mediante WordNet.
- En v3, interfaz interactiva y botón para iniciar otra partida.

La frecuencia y la clasificación lingüística se calculan sobre la **palabra inglesa de origen**, incluso si la palabra jugada se traduce al español.

## Limitaciones conocidas al revisar el código

- La traducción con `TextBlob.translate()` depende de una funcionalidad antigua y puede fallar con versiones actuales de la biblioteca o del servicio. En v2/v3, si falla, el selector puede quedarse buscando indefinidamente otra palabra.
- Las versiones de consola no validan estrictamente que el usuario introduzca una sola letra ni evitan todos los intentos repetidos.
- En v3, cambiar el idioma durante una partida no genera automáticamente otra palabra; el idioma visible y el de la palabra pueden no coincidir hasta reiniciar.
- En v3, la comprobación de letras repetidas no detecta correctamente los aciertos anteriores.
- Las etiquetas gramaticales y semánticas son aproximaciones, no definiciones verificadas.
- No hay pruebas automatizadas en el repositorio y no se ha comprobado la ejecución completa de las tres versiones.

## Estado del proyecto

Se conserva como proyecto histórico con una evolución visible: **consola original (2020) → consola bilingüe con análisis lingüístico (2025) → aplicación web Streamlit (2025)**. La reorganización del repositorio es documental; no supone correcciones funcionales.
