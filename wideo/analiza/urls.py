from django.urls import path
from .services import audio_analis
from .services import text_analis
from . import views

app_name='wideo'

urlpatterns =[
    path('czek/', views.index, name='index'),
    path("", views.indyk, name='indyk'),
    path("obróbka/", views.obróbka, name='obróbka')
  # path('extract_audio_from_video/', audio_analis.extract_audio_from_video, name='extract_audio_from_video'),
   # path('transcribe_audio/', audio_analis.transcribe_audio, name='transcribe_audio'),
   #path('analyze_volume/', audio_analis.analyze_volume, name='analyze_volume'),
   # path('analyze_background/', audio_analis.analyze_background, name='analyze_background'),
   #path('analyze_pauses/', text_analis.analyze_pauses, name='analyze_pauses'),
  # path('calculate_gunning_fog/', text_analis.calculate_gunning_fog, name='calculate_gunning_fog'),
   #path('analyze_emotions/', text_analis.analyze_emotions, name='analyze_emotions'),
  # path('check_transcription_agreement/', text_analis.check_transcription_agreement, name='check_transcription_agreement'),
   #path('analyze_text/', text_analis.analyze_text, name='analyze_text'),
   #path('detect_passive_voice/', text_analis.detect_passive_voice, name='detect_passive_voice'),
    #path('link/', views.link, name='link')
]