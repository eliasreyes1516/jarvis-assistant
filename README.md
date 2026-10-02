# JARVIS Assistant

Un asistente virtual tipo JARVIS para tu computadora, hecho en Python. Escucha tu voz, reconoce comandos y responde con voz.

## Características

- Reconocimiento de voz en español
- Respuesta con voz mediante TTS
- Apertura de sitios web
- Consulta de hora y fecha
- Comandos básicos de sistema
- Fácil de ampliar con nuevas funciones

## Requisitos

- Python 3.10+
- Micrófono
- Windows, Linux o macOS

## Instalación

```bash
pip install -r requirements.txt
```

Si en tu sistema aparece un error con `pyaudio`, instala primero el paquete del sistema:

- Windows: normalmente funciona con el paquete de Python directamente.
- Linux (Ubuntu/Debian):

```bash
sudo apt install portaudio19-dev python3-pyaudio
```

- macOS:

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
- "busca inteligencia artificial"
- "apágate" o "salir"

## Personalización

Puedes ampliar la lógica en el archivo `main.py` para:

- abrir apps del sistema
- controlar navegador
- consultar clima o noticias
- hablar con una API de IA
- crear una interfaz gráfica

