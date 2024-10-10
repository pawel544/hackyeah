from django.shortcuts import render
from django.http import HttpResponse
import logging


# Create your views here.
logging.basicConfig(level=logging.INFO)
def index(request):
    return render(request, 'analiza/czek.html')


def link(request):
    if request.method=='POST':
        audio_path= request.POST.get('audio_path')
        if audio_path:
            return HttpResponse(f"Trwa generowanie raportu. Dla pliku{audio_path}")
    else:
        return HttpResponse("Błędny adres URLS wprowdź poprawny", status=400)
    return HttpResponse("Błędny adres URLS wprowdź poprawny", status=400)



