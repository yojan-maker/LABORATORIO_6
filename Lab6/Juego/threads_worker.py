 threads_worker.py
import threading
import time
import random

class EnemyThread(threading.Thread):
    """
    Hilo que representa a un enemigo que patrulla horizontalmente
    entre left_limit y right_limit, con su 'y' fijo sobre la plataforma.
    Reporta su posición en state_queue como ("enemy_pos", id, x, y)
    y envía ("enemy_dead", id) cuando termina.
    """
    def __init__(self, id_, start_x, start_y, left_limit, right_limit,
                 state_queue, stop_event, position_lock, semaphore):
        super().__init__(daemon=True)
        self.id = id_
        self.x = float(start_x)
        self.y = int(start_y)
        self.left_limit = int(left_limit)
        self.right_limit = int(right_limit)
        # velocidad aleatoria ligera
        self.vx = random.choice([-1,1]) * (1.0 + random.random()*1.2)

        self.state_queue = state_queue
        self.stop_event = stop_event
        self.position_lock = position_lock
        self.semaphore = semaphore

    def run(self):
        # intentar adquirir semáforo; si no, terminar rápido
        acquired = self.semaphore.acquire(timeout=1)
        if not acquired:
            # indicar que este hilo no pudo activarse
            with self.position_lock:
                self.state_queue.put(("enemy_dead", self.id))
            return

        try:
            while not self.stop_event.is_set():
                # patrullar límites
                self.x += self.vx
                if self.x < self.left_limit:
                    self.x = self.left_limit
                    self.vx *= -1
                if self.x > self.right_limit:
                    self.x = self.right_limit
                    self.vx *= -1

                # reportar posición (usa la cola para comunicarse con el hilo principal)
                with self.position_lock:
                    self.state_queue.put(("enemy_pos", self.id, int(self.x), int(self.y)))

                time.sleep(0.020 + random.random()*0.02)
        finally:
 # liberar semáforo y notificar que el hilo finalizó
            try:
                self.semaphore.release()
            except Exception:
                pass
            with self.position_lock:
                self.state_queue.put(("enemy_dead", self.id))
