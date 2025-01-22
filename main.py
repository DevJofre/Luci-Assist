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
