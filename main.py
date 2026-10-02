import datetime
import os
import subprocess
import sys
import webbrowser
from typing import Optional

import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class Jarvis:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def speak(self, text: str):
        print(f"JARVIS: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception:
            # Si TTS falla, no interrumpe la ejecución.
            pass

    def listen(self):
        with sr.Microphone() as source:
            print("Escuchando...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio, language="es-MX")
            print(f"Tú: {text}")
            return text.lower()
        except sr.UnknownValueError:
            self.speak("No entendí lo que dijiste.")
            return ""
        except sr.RequestError:
            self.speak("No pude conectar con el servicio de voz.")
            return ""

    def open_url(self, url: str):
        webbrowser.open(url)

    def open_app(self, app_name: str):
        app_map = {
            "notepad": "notepad.exe" if os.name == "nt" else "notepad",
            "calculadora": "calc" if os.name == "nt" else "open -a Calculator",
            "explorer": "explorer" if os.name == "nt" else "open /Applications/Calculator.app",
            "terminal": "cmd" if os.name == "nt" else "gnome-terminal" if sys.platform.startswith("linux") else "open -a Terminal",
        }

        target = app_map.get(app_name.lower())
        if not target:
            self.speak(f"No encontré la aplicación {app_name}.")
            return

        try:
            if os.name == "nt":
                subprocess.Popen(target)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", "-a", app_name])
            else:
                if target.startswith("open "):
                    subprocess.Popen(target, shell=True)
                else:
                    subprocess.Popen(target)
            self.speak(f"Abriendo {app_name}.")
        except Exception:
            self.speak(f"No pude abrir {app_name}.")

    def shutdown_system(self):
        try:
            if os.name == "nt":
                subprocess.run(["shutdown", "/s", "/t", "1"], check=False)
            elif sys.platform == "darwin":
                subprocess.run(["osascript", "-e", 'tell app "System Events" to shut down'], check=False)
            else:
                subprocess.run(["sudo", "shutdown", "-h", "now"], check=False)
            self.speak("Apagando el sistema.")
        except Exception:
            self.speak("No puedo apagar el sistema desde aquí.")

    def reboot_system(self):
        try:
            if os.name == "nt":
                subprocess.run(["shutdown", "/r", "/t", "1"], check=False)
            elif sys.platform == "darwin":
                subprocess.run(["osascript", "-e", 'tell app "System Events" to restart'], check=False)
            else:
                subprocess.run(["sudo", "reboot"], check=False)
            self.speak("Reiniciando el sistema.")
        except Exception:
            self.speak("No puedo reiniciar el sistema desde aquí.")

    def ask_ai(self, question: str) -> str:
        if not self.client:
            return "No tengo una clave de OpenAI configurada. Puedes agregar OPENAI_API_KEY en tu archivo .env."

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres un asistente útil y amigable llamado JARVIS. Responde en español, de forma breve y útil."},
                    {"role": "user", "content": question},
                ],
                temperature=0.7,
                max_tokens=250,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            return f"No pude consultar la IA: {exc}"

    def help_text(self):
        return (
            "Comandos disponibles: hola, hora, fecha, abre google, abre youtube, "
            "abre notepad, abre calculadora, busca algo, pregunta algo, ayuda, salir."
        )

    def handle_command(self, command: str):
        if not command:
            return True

        if "hola" in command or "buenas" in command:
            self.speak("Hola, soy JARVIS. ¿En qué puedo ayudarte?")

        elif "ayuda" in command or "comandos" in command:
            self.speak(self.help_text())

        elif "hora" in command:
            current_time = datetime.datetime.now().strftime("%H:%M")
            self.speak(f"La hora es {current_time}.")

        elif "fecha" in command:
            current_date = datetime.datetime.now().strftime("%d de %B del %Y")
            self.speak(f"Hoy es {current_date}.")

        elif "abre google" in command:
            self.speak("Abriendo Google.")
            self.open_url("https://www.google.com")

        elif "abre youtube" in command:
            self.speak("Abriendo YouTube.")
            self.open_url("https://www.youtube.com")

        elif "abre notepad" in command or "abre bloc de notas" in command:
            self.open_app("notepad")

        elif "abre calculadora" in command or "abre calculator" in command:
            self.open_app("calculadora")

        elif "abre terminal" in command:
            self.open_app("terminal")

        elif "busca" in command:
            query = command.replace("busca", "").strip()
            if not query:
                self.speak("¿Qué quieres buscar?")
                text = self.listen()
                if text:
                    query = text.replace("busca", "").strip()
            if query:
                self.speak(f"Buscando {query} en Google.")
                self.open_url(f"https://www.google.com/search?q={query.replace(' ', '+')}")

        elif "pregunta" in command or "quien" in command or "que" in command or "cómo" in command:
            question = command.replace("pregunta", "").replace("qué", "que").strip()
            if not question:
                self.speak("¿Qué quieres saber?")
                question = self.listen()
            if question:
                self.speak("Dejame pensar...")
                response = self.ask_ai(question)
                self.speak(response)

        elif "apaga" in command or "apágate" in command:
            self.shutdown_system()
            return False

        elif "reinicia" in command:
            self.reboot_system()
            return False

        elif "salir" in command or "adios" in command or "adiós" in command:
            self.speak("Hasta luego.")
            return False

        else:
            self.speak("No tengo ese comando todavía. Puedes decir ayuda para ver las opciones.")

        return True

    def run(self):
        self.speak("Sistema listo. Soy JARVIS. Puedes hablar conmigo.")
        while True:
            command = self.listen()
            if not command:
                continue
            should_continue = self.handle_command(command)
            if not should_continue:
                break


if __name__ == "__main__":
    assistant = Jarvis()
    assistant.run()


