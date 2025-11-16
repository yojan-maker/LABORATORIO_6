import streamlit as st
import threading
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import time

# --------------------------------------
#   DICCIONARIO DE SENTIMIENTOS
# --------------------------------------
positive_words = ["bueno", "excelente", "me gusto", "muy bueno", "bien", "me gusta", "genial", "me encanta", "feliz", "perfecto", "maravilloso"]
negative_words = ["malo", "triste", "no me gusta", "pesimo", "horrible", "malisimo", "feo", "bastante mal", "terrible", "pésimo", "odio", "defecto", "decepcionado"]

def classify_text(text):
    text_lower = text.lower()

    positive_hits = sum(word in text_lower for word in positive_words)
    negative_hits = sum(word in text_lower for word in negative_words)

    score = positive_hits - negative_hits

    if score > 0:
        label = "positivo"
    elif score < 0:
        label = "negativo"
    else:
        label = "neutral"

    return score, label

# Función que procesará un lote de comentarios con hilos
def process_batch(comments):
    results = []
    for c in comments:
        score, label = classify_text(c)
        results.append((c, score, label))
    return results


# --------------------------------------
#              APP STREAMLIT
# --------------------------------------
st.set_page_config(page_title="Analizador de Sentimientos con Hilos",
                   layout="centered")

st.title("🔍 Analizador de Sentimientos con Hilos (Python + Threading)")

st.write("Procesa comentarios en paralelo usando hilos. Clasifica en **positivo, negativo o neutral**.")

# Entrada de comentarios
input_text = st.text_area("Ingresa varios comentarios (uno por línea):", height=200)

uploaded_file = st.file_uploader("O sube un archivo .txt o .csv", type=["txt", "csv"])

comments = []

if input_text.strip():
    comments = input_text.strip().split("\n")

elif uploaded_file is not None:

    if uploaded_file.name.endswith(".txt"):
        comments = uploaded_file.read().decode("utf-8").split("\n")

    elif uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        comments = df.iloc[:, 0].astype(str).tolist()

# Botón de análisis
if st.button("Procesar Comentarios"):

    if not comments:
        st.warning("No hay comentarios para procesar.")
    else:

        st.write("⏳ Procesando en paralelo...")

        # --------------------------
        #   PROCESAMIENTO CON HILOS
        # --------------------------
        chunks = []  
        num_threads = 4
        size = len(comments) // num_threads + 1

        # dividir comentarios en subgrupos
        for i in range(0, len(comments), size):
            chunks.append(comments[i:i + size])
        results = []

        lock = threading.Lock()

        def worker(chunk):
            partial_results = process_batch(chunk)
            with lock:
                results.extend(partial_results)

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(worker, chunks)

        # Convertir a DataFrame
        df = pd.DataFrame(results, columns=["Comentario", "Score", "Sentimiento"])

        st.success("✔ Procesamiento terminado")

        st.dataframe(df)

        # Contadores
        col1, col2, col3 = st.columns(3)
        col1.metric("Positivos", sum(df["Sentimiento"] == "positivo"))
        col2.metric("Negativos", sum(df["Sentimiento"] == "negativo"))
        col3.metric("Neutrales", sum(df["Sentimiento"] == "neutral"))

        # Descargar resultados
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar resultados", csv, "sentimientos.csv", "text/csv")
