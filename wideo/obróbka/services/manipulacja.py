from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip
import logging

def konkantynacja(list_clip:list,poz:list=None )->None:
    """
       Łączy klipy wideo w jeden plik i zapisuje go jako nowy plik.

       Parametry:
           list_clip (list): Lista ścieżek do plików wideo, które mają być połączone.
           poz (list): Lista krotek z pozycjami (pozy1, pozy2) dla każdego klipu.
                       Jeśli None lub liczba pozycji nie zgadza się z liczbą klipów,
                       klipy zostaną połączone liniowo (concatenate_videoclips).
       """
    try:
        clip = [VideoFileClip(ścieżka) for ścieżka in list_clip]
        if poz is not None and len(poz)== len(clip):
            finly_clip= CompositeVideoClip([c.set_position(p) for c,p in zip(clip,poz)])
            logging.info("Ustawiono pozycje dla klipów.")
        else:
            finly_clip= concatenate_videoclips(clip)
            logging.info("Klipy zostały połączone liniowo.")
        finly_clip.write_videofile("last_clip.mp4")
        logging.info(f"Konkatynacja zakończona")
    except Exception as e:
        logging.error(f"Błąd {e}")
    finally:
        for _ in clip:
           _.close()
        logging.info("zakończenie wideo")

def cut(plik_wideo:str,start:int, end:int)->None:
    """
        Wycina fragment wideo od momentu 'start' do 'end' i zapisuje go jako nowy plik.

        Parametry:
            plik_wideo (str): Ścieżka do pliku wideo, który ma być przycięty.
            start (int): Początek wycinanego fragmentu (w sekundach).
            end (int): Koniec wycinanego fragmentu (w sekundach).
        """
    try:
        finly_clip=VideoFileClip(plik_wideo).subclip(start,end)
        finly_clip.write_videofile("list_clip.mp4", codec="libx264")
        logging.info(f"Wycinanie zakończone")
    except Exception as e:
        logging.error(f"Błąd {e}")
    finally:
        if finly_clip is not None:
            finly_clip.close()
        logging.info("Zakończenie wideo")