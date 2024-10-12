import cv2


def odtwarzcz(path):
    cap= cv2.VideoCapture(path)
    if not cap.isOpened():
        print("Błąd podczas ładowania spróbuj ponownie")
        exit()
    else:
        while cap.isOpened():
            ret, frame= cap.read()

            if not ret:
                print('Konie odtważania')

            cv2.imshow('obróbka_wideo',frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()