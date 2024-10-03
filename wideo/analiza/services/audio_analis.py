import speech_recognition as sr
from deepface import DeepFace

def extract_audio_from_video(video_path: str, audio_path: str) -> None:
    """Ekstrahuje audio z pliku wideo."""
    try:
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path)
        logging.info(f"Audio wyodrębnione z {video_path} do {audio_path}")
    except Exception as e:
        logging.error(f"Błąd przy ekstrakcji audio: {e}")

def transcribe_audio(audio_path: str) -> str:
    """Transkrybuje audio do tekstu."""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            return recognizer.recognize_google(audio_data, language='pl-PL')
    except sr.UnknownValueError:
        logging.error("Nie udało się rozpoznać mowy.")
        return "Nie udało się rozpoznać mowy"
    except sr.RequestError as e:
        logging.error(f"Błąd żądania: {e}")
        return "Błąd żądania"
    except Exception as e:
        logging.error(f"Błąd podczas transkrypcji: {e}")
        return "Błąd podczas transkrypcji"

def analyze_volume(audio_path: str, quiet_threshold: float = 0.01, loud_threshold: float = 0.1) -> dict:
    """Analizuje poziom głośności w pliku audio."""
    try:
        y, sr = librosa.load(audio_path, sr=None)
        rms = librosa.feature.rms(y=y)[0]
        loudness = np.mean(rms)
        volume_status = "normalny"
        if loudness < quiet_threshold:
            volume_status = "za cicho"
        elif loudness > loud_threshold:
            volume_status = "za głośno"

        logging.info(f"Analiza głośności zakończona. Głośność: {volume_status}")
        return {
            'Poziom głośności (RMS)': loudness,
            'Status głośności': volume_status,
        }
    except Exception as e:
        logging.error(f"Błąd podczas analizy głośności: {e}")
        return {'Poziom głośności (RMS)': 0, 'Status głośności': 'Błąd analizy'}

def analyze_background(video_path: str, frame_skip: int = 10) -> str:
    """Analizuje tło wideo."""
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logging.error("Nie udało się otworzyć wideo.")
            return "Błąd otwierania wideo"

        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)

        cap.release()
        mp_face_detection = mp.solutions.face_detection
        with mp_face_detection.FaceDetection(min_detection_confidence=0.2) as face_detection:
            detected_faces = []
            for frame in frames[::frame_skip]:
                results = face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                if results.detections:
                    detected_faces.append(len(results.detections))

            if detected_faces:
                average_faces = sum(detected_faces) / len(detected_faces)
                return f"Średnia liczba wykrytych twarzy: {average_faces:.2f}"
            else:
                return "Nie wykryto twarzy w tło."
    except Exception as e:
        logging.error(f"Błąd podczas analizy tła: {e}")
        return "Błąd podczas analizy tła"