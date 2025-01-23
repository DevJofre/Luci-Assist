import os
from dotenv import load_dotenv
import speech_recognition as sr
import pygame
from pygame import mixer
import tempfile
import edge_tts
import time
from groq import Groq

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError(
        "A chave GROQ_API_KEY não foi encontrada. Verifique o arquivo .env.")

client = Groq(api_key=groq_api_key)

chat_model = "gema2-9b-isto"
voice_model = "pt-BR-AntonioNeural"
temperature = 0.5
voice_speed = '+50%'
personalidade = "Seu nome e Luci, você sempre me chama de senhor, mas meu nome e Jofre."


def main():
    list_mensg = []
    list_mensg.append(
        {"role": "system", "content": "Sua personalidade é: {personalidade}"})

    while True:
        time.sleep(0.1)

        text = speech_to_text()

        if text == 1:
            break
        else:
            text_generetion(text, list_mensg, chat_model,
                            voice_model, temperature, voice_speed)


def speech_to_text():
    r = sr.Recognizer()
    print("\n\nChatbot ativado. Diga 'sair' para encerrar.\n")

    try:
        with sr.Microphone() as source:
            print("Ouvindo...")
            r.adjust_for_ambient_noise(source)
            audio_data = r.listen(source)
            texto = r.recognize_google(audio_data, language="pt-BR")
            print("Você disse: " + texto)

            if texto.lower() == "sair":
                print("Encerrando o chatbot.")
                return 1
            return texto
    except sr.UnknownValueError:
        print("Não entendi o que você disse. Tente novamente.")

    except sr.RequestError as e:
        print(f"Erro no serviço de reconhecimento de voz; {e}")
