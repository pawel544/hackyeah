import numpy as np
import re


def analyze_pauses(audio_path: str, pause_threshold: float = 1.0) -> list:
    """Analizuje długie pauzy w mowie."""
    try:
        y, sr = librosa.load(audio_path, sr=None)
        intervals = librosa.effects.split(y, top_db=30)
        pauses = []
        for i in range(len(intervals) - 1):
            start = intervals[i][1]
            end = intervals[i + 1][0]
            pause_duration = (end - start) / sr
            if pause_duration > pause_threshold:
                pauses.append(pause_duration)
                logging.info(f"Pauza o długości {pause_duration:.2f} sekund wykryta.")
        return pauses
    except Exception as e:
        logging.error(f"Błąd podczas analizy pauz: {e}")
        return []

def calculate_gunning_fog(text: str) -> float:
    """Oblicza wskaźnik Gunning-Fog dla danego tekstu."""
    words = text.split()
    complex_words = [word for word in words if len(word) > 7]
    avg_sentence_length = len(words) / max(1, text.count('.') + text.count('!') + text.count('?'))
    return 0.4 * ((avg_sentence_length) + 100 * (len(complex_words) / len(words)))

def detect_false_words(text: str) -> list:
    """Wykrywa nieprawdziwe słowa w tekście."""
    false_words = ["fałsz", "kłamstwo", "nieprawdziwy", "niewłaściwy"]  # Przykładowe słowa
    found_words = [word for word in false_words if word in text.lower()]
    return found_words

def analyze_emotions(text: str) -> dict:
    """Analizuje emocje w tekście."""
    emotion_pipeline = pipeline("text-classification", model="bhadresh-savani/emotion-analysis")
    return emotion_pipeline(text)

def check_transcription_agreement(transcription: str, audio_path: str) -> dict:
    """Sprawdza zgodność transkrypcji z audio."""
    try:
        original_text = transcribe_audio(audio_path)
        original_words = original_text.split()
        transcription_words = transcription.split()

        d = difflib.Differ()
        diff = list(d.compare(original_words, transcription_words))

        discrepancies = [word for word in diff if word.startswith('- ')]
        matches = [word for word in diff if word.startswith('+ ')]

        return {
            'Zgodność': len(discrepancies) == 0,
            'Różnice': discrepancies,
            'Dopasowania': matches,
            'Liczba różnic': len(discrepancies),
        }
    except Exception as e:
        logging.error(f"Błąd podczas sprawdzania zgodności transkrypcji: {e}")
        return {
            'Zgodność': False,
            'Różnice': [],
            'Dopasowania': [],
            'Liczba różnic': 0,
        }

def analyze_text(text: str, audio_path: str) -> dict:
    """Analizuje tekst pod kątem zrozumiałości i błędów."""
    try:
        readability_score = textstat.flesch_reading_ease(text)
        gunning_fog_index = calculate_gunning_fog(text)
        language = detect(text)

        y, sr = librosa.load(audio_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)

        errors = {
            "przerywniki": len(re.findall(r'\b(um|uh|no|like|tak|więc|wiesz|ej|yyy|eee|hmm|mhm)\b', text)),
            "za_szybkie_tempo": len(text.split()) / (duration / 60) > 150,
            "powtórzenia": sum(text.count(word) > 1 for word in set(text.split())),
            "zmiana_tematu": len(re.findall(r'\b(teraz|przechodząc|wracając|w międzyczasie|na inny temat)\b', text)),
            "za_dużo_liczb": len(re.findall(r'\d+', text)) > 10,
            "długie_słowa": sum(len(word) > 15 for word in text.split()),
            "trudne_słowa": len(re.findall(r'\b\w{12,}\b', text)),
            "żargon": len(re.findall(r'\b(technologia|interfejs|algorytm|wymiana)\b', text)),
            "obcy_język": language != 'pl',
            "za_długa_pauza": analyze_pauses(audio_path),
            "akcentowanie": len(re.findall(r'\b(nie|tak|to|właśnie|rzeczywiście)\b', text)),
            "trudne_zdania": len([sentence for sentence in re.split(r'[.!?]', text) if len(sentence.split()) > 20]),
            "zgodność_z_transkrypcją": check_transcription_agreement(text, audio_path),
            "strona_bierna": detect_passive_voice(text),
        }

        sentiment = TextBlob(text).sentiment
        logging.info("Analiza tekstu zakończona.")

        return {
            'Wskaźnik czytelności': readability_score,
            'Indeks mglistości': gunning_fog_index,
            'Język': language,
            'Błędy': errors,
            'Sentyment': sentiment,
            'Nieprawdziwe słowa': detect_false_words(text),
            'Emocje': analyze_emotions(text),
        }
    except Exception as e:
        logging.error(f"Błąd podczas analizy tekstu: {e}")
        return {}

def detect_passive_voice(text: str) -> bool:
        """Wykrywa zdania w stronie biernej."""
        passive_voice_indicators = ["być", "zostać", "będzie", "jest", "są"]
        return any(phrase in text for phrase in passive_voice_indicators)