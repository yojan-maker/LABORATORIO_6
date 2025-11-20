# ⚙️ Laboratorio 6

Este repositorio contiene las prácticas desarrolladas para el laboratorio 6
1. **Análisis de sentimientos** (texto e imágenes).
2. **Juego platformer** en Pygame con concurrencia.
3. 
---

## 🎯 Objetivo del Proyecto

El objetivo principal es demostrar la aplicación de técnicas de concurrencia y sincronización en problemas reales:

* **Técnicas de Concurrencia:** Hilos (`threading.Thread`).
* **Sincronización:** Bloqueos (`Lock` / sección crítica).
* **Control de Concurrencia:** Semáforos (`Semaphore`).

Estas técnicas se utilizan para el **procesamiento paralelo** de texto/imágenes y la gestión de **entidades simultáneas** en un juego.

---

## 📝 Contenido del README

Este documento está estructurado para guiarte paso a paso:

1.  Requisitos y preparación del entorno.
2.  Ejecución y Explicación de cada entregable.
3.  Detalle de dónde se usan hilos / mutex / semáforos.
4.  Cómo probar y demostrar el funcionamiento.

> **Nota:** El proyecto está dividido en módulos. Se recomienda seguir el orden para la ejecución:
> 1.  Análisis de sentimientos (script principal)
> 2.  Juego platformer
> 3.  App Streamlit 

---

## 💻 Requisitos

### Requisitos de Sistema (Recomendados)

| Requisito | Detalle |
| :--- | :--- |
| **Sistema Operativo** | Ubuntu 20.04 / 22.04 (Probado en Linux) |
| **CPU** | Soporte SSE (cualquier PC moderno) |
| **Python** | 3.10 — 3.12 (Recomendado 3.10/3.11 para máxima compatibilidad) |
| **Para Dockerizar** | Docker |
| **Gráficos** | OpenGL (para PyBullet / visualización de simuladores si se usan) |

### Dependencias Python (por proyecto)

Se **recomienda crear un entorno virtual (`venv`)** para cada entrega para evitar conflictos de dependencias.

### 1) Análisis de sentimientos (Texto y Pipeline)

Las dependencias principales para esta sección son:

* `pandas`
* `streamlit` (si se va a usar la aplicación web)

**Archivo de dependencias sugerido:**
  `requirements_sentiment.txt`

---

 ### 2) Juego platformer Pygame
 Para el juego solo se requiere:
 * `pygame`

Archivo recomendado:
`requirements_juego.txt`

---
### 3)

---

## 🧩 1. Análisis de Sentimientos por Texto (Con Hilos, Mutex y Semáforos)

En este entregable se implementa un **analizador de sentimientos** que clasifica textos como:

*  **Positivo**
*  **Negativo**
*  **Neutral**

También cuenta con la posibilidad de analizar sentimientos a través de archivos .txt y cuenta con la posibilidad de descargar los resultados
del análisis

El procesamiento se realiza usando **concurrencia** para analizar múltiples textos en paralelo, demostrando el uso de:

| Componente | Uso en el Código | Propósito |
| :--- | :--- | :--- |
| **✔ Hilos** (`threading.Thread`) | Ejecución de tareas paralelas. | Procesar cada texto de forma independiente. |
| **✔ Mutex** (`Lock`) | Protección de la sección crítica. | Evitar condiciones de carrera al escribir resultados. |
| **✔ Semáforos** (`Semaphore`) | Control de concurrencia. | Limitar cuántos hilos trabajan simultáneamente. |

---

### ⚙️ Instalación

Se recomienda crear un entorno virtual para aislar las dependencias:

1.  **Crear y activar entorno virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  **Instalar dependencias necesarias:**
    ```bash
    pip install pandas streamlit textblob
    ```
    *(Nota: `textblob` es necesaria para la funcionalidad de análisis de sentimiento mostrada en el ejemplo.)*

---

### ▶️ Ejecución

Este módulo se puede ejecutar de dos maneras:

| Opción | Comando | Descripción |
| :--- | :--- | :--- |
| **A: Consola** | `python sentimientos.py` | Ejecuta el script principal que procesa la lista de textos. |
| **B: Interfaz Web** | `streamlit run app_sentimientos.py` | Lanza la aplicación web interactiva. |

---

### 🧠 ¿Cómo funciona?

El usuario ingresa varios textos en la interfaz de Streamlit.
Cuando presiona Procesar, se realiza lo siguiente:

Cada texto se envía a un hilo independiente

El semáforo define cuántos hilos pueden ejecutarse simultáneamente
(por ejemplo, máximo 2 textos procesándose a la vez)

Cada hilo calcula el sentimiento:
- 😄 Positivo
- 😡 Negativo
- 😐 Neutral

Se usa un mutex (Lock) para que solo un hilo a la vez escriba en los resultados

Streamlit muestra los resultados en pantalla de manera ordenada
- #### 🧵 Uso de HILOS

Cada texto es procesado por un hilo independiente, inicializado y lanzado de la siguiente manera:

```python
hilo = threading.Thread(target=procesar_texto, args=(texto, i, resultados, lock, semaforo))
hilo.start()
```
Ejemplo: Si hay 3 textos, se lanzan 3 hilos. Al usar t.join(), el programa principal espera a que todos terminen.

- #### 🔒 Uso de MUTEX (Lock)

El Mutex se usa para proteger la sección crítica, asegurando que solo un hilo a la vez pueda modificar la estructura de resultados
(resultados.append(...)).

```python
# Sección crítica
with lock:
    resultados.append({"id": index, "texto": texto, "sentimiento": sentimiento})
```
Esto evita: resultados corruptos, salidas mezcladas y condiciones de carrera.

- #### 🚦 Uso de SEMÁFORO

El Semáforo controla el número máximo de hilos que pueden estar activos y ejecutándose en la sección de procesamiento pesado (simulado con time.sleep(1)).

```python
# Permite un máximo de 2 hilos activos al mismo tiempo
semaforo = threading.Semaphore(2)

# Antes de procesar (espera si el límite está lleno)
semaforo.acquire()

# Al finalizar (libera un espacio para otro hilo)
semaforo.release()
```

- #### 📤 Ejemplo de Salida en Consola

1. Ingresas:
- Bueno
- Horrible
- Más o menos

La app procesa los textos en paralelo

Muestra:
```python
➡️ Me siento feliz hoy. → POSITIVO
➡️ Esto es horrible. → NEGATIVO
➡️ Es un día normal. → NEUTRAL
```

- #### 🧷 Conclusión de este módulo
Este módulo es una demostración efectiva del uso de:

 Este módulo demuestra:

✔ Concurrencia real aplicada

✔ Uso de hilos para paralelizar tareas

✔ Protección de datos con mutex

✔ Control de carga con semáforo

✔ Interfaz moderna con Streamlit

✔ Implementación práctica en procesamiento de texto

✔ Dockerización

El resultado es una ejecución fluida, paralela y segura del análisis de sentimientos.


![Image](https://github.com/user-attachments/assets/d38fcbb2-e87c-4489-baa9-43fedf50d259)

![Image](https://github.com/user-attachments/assets/f4cb6160-9066-49a7-acfd-5f1bb01c8845)

---
## 🎮 2. Juego Platformer (Pygame + Concurrencia)

El segundo entregable del laboratorio es un juego tipo **platformer** creado con **Pygame**. El objetivo es aplicar las técnicas de **hilos**, **mutex** y **semáforos** para controlar acciones simultáneas dentro de un entorno de juego en tiempo real.

Este módulo demuestra cómo los mecanismos de concurrencia permiten manejar eventos paralelos de forma fluida y segura.

---

### 🧩 ¿Qué hace este módulo?

Este juego utiliza la concurrencia para separar el *game loop* principal de la generación dinámica de entidades:

* **✔ Hilo Principal:** Controla el movimiento del jugador, renderiza la pantalla y procesa las colisiones en tiempo real.
* **✔ Hilo Secundario:** Ejecuta un proceso independiente encargado de generar y aparecer obstáculos/enemigos.
* **✔ Locks:** Usados para proteger las **listas compartidas** de enemigos.
* **✔ Semáforos:** Usados para **limitar** cuántos enemigos pueden existir en el nivel al mismo tiempo.
* **✔ Dockerización** 


El flujo de trabajo concurrente se estructura así:

| Hilo / Componente | Función Principal |
| :--- | :--- |
| **Hilo 1** (Loop Principal) | Renderiza pantalla, mueve jugador, detecta colisiones. |
| **Hilo 2** (Generador) | Genera enemigos, limitado por el semáforo, e inserta en la lista compartida. |
| **Elemento Compartido** | Lista de enemigos. |

---

- ### 🕹️ 2.1 Código Base del Platformer

**Archivo sugerido:** `platformer.py`

Este juego integra los siguientes componentes de concurrencia de Python:

* `threading.Thread`
* `threading.Semaphore`
* `threading.Lock`
* `Lista compartida de enemigos`
* `Hilo principal con Pygame (Interfaz)`
* `Hilo secundario generando enemigos (Lógica)`

---

- ### 🔐 2.2 ¿Dónde usamos concurrencia y sincronización?

| Elemento | Uso Específico | Propósito |
| :--- | :--- | :--- |
| **Hilos** | Uno principal (juego), uno secundario (generando enemigos). | Separar la lógica de la interfaz y la generación de eventos. |
| **Lock** | Protege la lista `enemigos`. | Evitar **condiciones de carrera** al borrar/dibujar/modificar la lista desde hilos diferentes. |
| **Semáforo** | Controla el `acquire()` en el hilo generador. | Limita el número máximo de enemigos simultáneos en pantalla. |
| **Sección Crítica** | Acceso a la lista `enemigos` en ambos hilos. | Zona de código donde se requiere la protección del `Lock`. |
| `daemon=True` | Aplicado al hilo generador. | Permite que el hilo secundario se cierre automáticamente al salir del juego principal. |

---

- ### ▶️ 2.3 ¿Cómo se ejecuta?

Simplemente ejecuta el archivo principal del platformer usando Python 3:

```bash
python3 platformer.py
```

- #### 📦 2.4 Requisitos
 El único requisito adicional para ejecutar la interfaz del juego es la librería Pygame.
 Archivo sugerido: requirements_platformer.txt
 ```bash
pygame
```
![Image](https://github.com/user-attachments/assets/3153d7a1-9042-4228-82e6-d2bed04ba69c)

![Image](https://github.com/user-attachments/assets/dd2064d9-0ee8-41f0-8f80-3ca73db4c818)

![Image](https://github.com/user-attachments/assets/d75703b2-27c3-435f-941e-37d3a9083b60)

![Image](https://github.com/user-attachments/assets/7c2cba29-69a2-4148-a647-5e7423067c2c)

---

### 3) ✋🤖 Detector de Gestos con MediaPipe, Hilos y Docker

En este laboratorio se implementó un sistema capaz de detectar gestos de mano en tiempo real utilizando visión por computadora, sincronización con hilos y despliegue en contenedores Docker.
A continuación se explica de forma clara cómo se construyó este módulo del proyecto.
