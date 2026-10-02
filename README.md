# JARVIS Assistant

Un asistente virtual avanzado inspirado en JARVIS, con reconocimiento de voz, texto a voz, automatización básica del sistema y soporte opcional para IA con OpenAI.

## Características

- Reconocimiento de voz en español
- Respuesta por voz (TTS)
- Búsqueda en Google
- Apertura de sitios web
- Apertura de aplicaciones del sistema
- Consulta de hora y fecha
- Soporte opcional con OpenAI para responder preguntas más complejas
- Fácil de ampliar

## Requisitos

- Python 3.10+
- Micrófono
- Windows, Linux o macOS

## Instalación

1. Clona o descarga este proyecto.
2. Instala dependencias:

```bash
pip install -r requirements.txt
```

3. Crea un archivo `.env` basado en `.env.example`:

```bash
cp .env.example .env
```

4. Si quieres usar IA con OpenAI, agrega tu clave:

```env
OPENAI_API_KEY=tu_clave_aqui
```

## Si falla `pyaudio`

### Windows
Normalmente funciona con pip directamente.

### Linux (Ubuntu/Debian)

```bash
sudo apt install portaudio19-dev python3-pyaudio
```

### macOS

```bash
brew install portaudio
```

## Ejecutar

```bash
python main.py
```

## Comandos de ejemplo

- "hola"
- "qué hora es"
- "qué fecha es"
- "abre google"
- "abre youtube"
- "abre notepad"
- "abre calculadora"
- "busca inteligencia artificial"
- "pregunta ¿qué es la programación?"
- "ayuda"
- "salir"

## Notas

- Si no agregas `OPENAI_API_KEY`, JARVIS seguirá funcionando con comandos básicos.
- La IA solo se usa cuando tú preguntes algo o le digas "pregunta ...".

## Personalización

Puedes expandir el proyecto para:

- abrir más programas del sistema
- controlar navegador con más precisión
- consultar clima
- usar funciones de escritorio automatizadas
- integrar una interfaz gráfica tipo HUD

