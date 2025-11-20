import cv2
import threading
from threading import Semaphore, Lock
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
mutex = Lock()
sem_frame = Semaphore(0)
stop_flag = False

frame_global = None
resultado_global = None
def hilo_captura():
    global frame_global, stop_flag

    cap = cv2.VideoCapture(0)

    while not stop_flag:
        ret, frame = cap.read()
        if not ret:
            continue

        with mutex:
            frame_global = frame.copy()

        sem_frame.release()

    cap.release()
  def hilo_procesar():
    global resultado_global, stop_flag

    base_options = python.BaseOptions(
        model_asset_path="gesture_recognizer.task"
    )
    options = vision.GestureRecognizerOptions(base_options=base_options)
    recognizer = vision.GestureRecognizer.create_from_options(options)

    while not stop_flag:
        sem_frame.acquire()

        with mutex:
            if frame_global is None:
                continue
            frame_local = frame_global.copy()

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_local)
        result = recognizer.recognize(mp_image)

        with mutex:
            resultado_global = result
t1 = threading.Thread(target=hilo_captura, daemon=True)
t2 = threading.Thread(target=hilo_procesar, daemon=True)

t1.start()
t2.start()

print("Detector iniciado. Presiona CTRL + C para detener.")

try:
    while True:
        if resultado_global is not None:
            gesture = resultado_global.gestures[0][0]
            print(f"Gesto detectado: {gesture.category_name}  | Score: {gesture.score:.2f}")
except KeyboardInterrupt:
    stop_flag = True
    print("Cerrando...")
