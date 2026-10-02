import datetime
import os
import subprocess
import sys
import webbrowser

import pyttsx3
import speech_recognition as sr


class Jarvis:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)

    def speak(self, text: str):
        print(f"JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

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

    def handle_command(self, command: str):
        if not command:
            return True

        if "hola" in command or "buenas" in command:
            self.speak("Hola, soy JARVIS. ¿En qué puedo ayudarte?")
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
        elif "busca" in command:
            query = command.replace("busca", "").strip()
            if query:
                self.speak(f"Buscando {query} en Google.")
                self.open_url(f"https://www.google.com/search?q={query.replace(' ', '+')}")
            else:
                self.speak("¿Qué quieres buscar?")
                text = self.listen()
                if text:
                    self.open_url(f"https://www.google.com/search?q={text.replace(' ', '+')}")
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
            self.speak("No tengo ese comando todavía, pero puedo aprenderlo.")

        return True

    def run(self):
        self.speak("Sistema listo. Puedes hablar conmigo.")
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
