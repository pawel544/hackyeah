from django.shortcuts import render
from django.http import HttpResponse
import logging
#import librosa
#import speech_recognition as sr
#from moviepy.editor import VideoFileClip
#import cv2
#from deepface import DeepFace
#import textstat
#from langdetect import detect
#import numpy as np
#import re
#from textblob import TextBlob
#from concurrent.futures import ThreadPoolExecutor

#import mediapipe as mp
#from transformers import pipeline
#import difflib
# Create your views here.
logging.basicConfig(level=logging.INFO)

def link(request):
    if request.method==POST:
        audio_path= request.POST.get('audio_path')
        if audio_path:
            return HttpResponse(f"Trwa generowanie raportu. Dla pliku{audio_path}")
    else:
        return HttpResponse("Błędny adres URLS wprowdź poprawny", status=400)
    return HttpResponse("Błędny adres URLS wprowdź poprawny", status=400)



