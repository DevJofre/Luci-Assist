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

chat_model = "mixtral-8x7b-32768"
voice_model = "pt-BR-AntonioNeural"
temperature = 0.5
velocidade_voz = '+50%'
personalidade = "Seu nome e Luci, você sempre me chama de senhor, mas meu nome e Jofre."


def main():

    lista_mensagens = []
    lista_mensagens.append({"role": "system", "content":
                            f"Sua personalidade é: {personalidade}"})
    while True:
        time.sleep(0.1)

        texto = speech_to_text()

        if texto == 1:
            break
        else:
            text_generation(texto, lista_mensagens, chat_model,
                            voice_model, temperature, velocidade_voz)


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


def text_generation(mensagem, lista_mensagens, chat_model, voice_model, temperature, velocidade_voz):

    if not mensagem:
        print("Mensagem vazia, tente novamente.")
        return

    lista_mensagens.append({"role": "user", "content": mensagem})

    response = client.chat.completions.create(
        model=chat_model,
        messages=lista_mensagens,
        stream=True)

    answer = ""
    accumulated_text = ""
    texto_final = ""

    print("Assistente: ", end='')

    for event in response:

        answer = event.choices[0].delta.content
        answer = answer or ""
        accumulated_text += answer
        texto_final += answer
        print(answer, end='', flush=True)

        if '.' in answer or ';' in answer or ':' in answer or '!' in answer or '?' in answer or (answer == "" and accumulated_text != ''):
            text_to_speech(accumulated_text, voice_model, velocidade_voz)
            accumulated_text = ""
            print()

    lista_mensagens.append({"role": "assistant", "content": texto_final})


def text_to_speech(mensagem_resposta, voice_model, velocidade):

    if mensagem_resposta != "":

        mensagem_resposta = mensagem_resposta.replace(
            "*", "").replace("#", "")

        with tempfile.NamedTemporaryFile(suffix=".opus", delete=True) as temp_file:
            file_path = temp_file.name

        communicate = edge_tts.Communicate(
            mensagem_resposta, voice_model, rate=velocidade)

        communicate.save_sync(file_path)

        pygame.mixer.init()
        sound = mixer.Sound(file_path)

        while pygame.mixer.get_busy():
            time.sleep(0.1)

        sound.play()


if __name__ == "__main__":
    main()
