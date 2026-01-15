import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import time
import random
import os
from datetime import datetime

# Configurare pagina si layout
st.set_page_config(page_title="SIA Trafic Pro - Poli Bucuresti", layout="wide")

# CSS pentru design si interfata vizuala
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    
    /* Stil pentru intersectia vizuala (patratele) */
    .intersection-container {
        display: grid;
        grid-template-columns: 100px 100px 100px;
        grid-template-rows: 100px 100px 100px;
        gap: 10px;
        justify-content: center;
        margin-bottom: 20px;
    }
    .road { background-color: #333; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;}
    .center { background-color: #555; border-radius: 50%; }
    
    /* Culori semafor */
    .light-red { background-color: #d9534f; box-shadow: 0 0 15px #d9534f; }
    .light-green { background-color: #5cb85c; box-shadow: 0 0 15px #5cb85c; }
    .light-yellow { background-color: #f0ad4e; box-shadow: 0 0 15px #f0ad4e; } /* NOU ETAPA 6 */
    
    /* Stil pentru casuta de explicatii (XAI) */
    .xai-box {
        background-color: #e8f4f8;
        color: #333333;
        border-left: 5px solid #007bff;
        padding: 15px;
        margin-top: 10px;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        font-weight: 600;
    }
    
    .decision-box { 
        padding: 20px; border-radius: 10px; text-align: center; 
        color: white; font-size: 24px; font-weight: bold;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Functie pentru logare in fisier (Black Box)
def log_decision(decision_text, reason_text, is_emergency, confidence):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] STATUS: {decision_text} | CONF: {confidence:.1f}% | MOTIV: {reason_text} | URGENTA: {is_emergency}\n"
    with open("blackbox.log", "a", encoding="utf-8") as f:
        f.write(log_entry)

# Incarcam modelul si scaler-ul antrenat
@st.cache_resource
def load_assets():
    # --- MODIFICARE ETAPA 6: Incarcam modelul OPTIMIZAT ---
    # Cautam intai modelul optimizat, daca nu exista, il luam pe cel vechi
    path_optimizat = 'models/optimized_model.h5'
    path_vechi = 'models/trained_model.h5'
    
    path_final = path_optimizat if os.path.exists(path_optimizat) else path_vechi
    
    model = tf.keras.models.load_model(path_final)
    scaler = joblib.load('config/preprocessing_params.pkl')
    return model, scaler, path_final

model, scaler, loaded_path = load_assets()

# Initializare variabile pentru sesiune
if 'history' not in st.session_state: st.session_state.history = []
if 'total_cars' not in st.session_state: st.session_state.total_cars = 0

# Titlu si Sidebar
st.title("🚦 Sistem Inteligent & Auditabil (SIA)")
st.caption(f"ℹ️ Model activ: `{os.path.basename(loaded_path)}`") # Afisam ce model folosim

st.sidebar.header("⚙️ Panou de Control")

mode = st.sidebar.radio("Mod de operare:", ["Manual", "Auto-Play"])
run_sim = False

# Configurare simulator
if mode == "Auto-Play":
    run_sim = st.sidebar.toggle("Porneste Simulare", value=True)
    refresh_speed = st.sidebar.slider("Viteza refresh (sec)", 1.0, 10.0, 3.0)

col1, col2 = st.columns([1, 2])

# Coloana stanga: Input date
with col1:
    st.subheader("Date de la Senzori")
    if mode == "Manual":
        ns_auto = st.slider("Vehicule N-S", 0, 100, 20)
        ev_auto = st.slider("Vehicule E-V", 0, 100, 20)
        ns_p = st.slider("Pietoni N-S", 0, 50, 0)
        ev_p = st.slider("Pietoni E-V", 0, 50, 0)
        sirena = st.toggle("🚨 Sirena Urgenta", value=False)
    else:
        # Generare valori random pentru simulare
        ns_auto = random.randint(0, 100)
        ev_auto = random.randint(0, 100)
        ns_p = random.randint(0, 50)
        ev_p = random.randint(0, 50)
        sirena = random.random() < 0.05 # 5% sansa de sirena
        
        c_a, c_b = st.columns(2)
        c_a.metric("Vehicule N-S", ns_auto)
        c_b.metric("Vehicule E-V", ev_auto)
        c_a.metric("Pietoni N-S", ns_p)
        c_b.metric("Pietoni E-V", ev_p)
        if sirena: st.error("🚨 DETECTIE SIRENA!")

# Pregatim datele pentru model (normalizare)
input_raw = np.array([[ns_auto/2, ns_auto/2, ev_auto/2, ev_auto/2, 
                        ns_p/2, ns_p/2, ev_p/2, ev_p/2, (1 if sirena else 0)]])
input_scaled = scaler.transform(input_raw)

# Facem predictia
prediction = model.predict(input_scaled, verbose=0)
clasa_ai = np.argmax(prediction)
confidenta = np.max(prediction) * 100

# --- MODIFICARE ETAPA 6: LOGICA AVANSATA DE DECIZIE ---
reason = ""
decision_label = ""
bg_color = "#d9534f" # Default Rosu

if sirena:
    final_decision = 0
    decision_label = "URGENTA - SIRENA"
    reason = "⚠️ PROTOCOL PRIORITATE: Am detectat vehicul interventie."
    bg_color = "#d9534f"
elif confidenta < 60.0:
    # INCERTITUDINE -> Trecem pe galben/rosu preventiv
    final_decision = -1 # Cod intern pentru incertitudine
    decision_label = "INCERTITUDINE - PRUDENTA"
    reason = f"⚠️ Incredere scazuta ({confidenta:.1f}%). Modelul ezita intre stari."
    bg_color = "#f0ad4e" # Galben
else:
    final_decision = clasa_ai
    if final_decision == 1:
        diff = ns_auto - ev_auto
        reason = f"OPTIMIZARE FLUX: Trafic N-S ({ns_auto}) > E-V ({ev_auto})."
        decision_label = "VERDE NORD-SUD"
        bg_color = "#5cb85c"
    elif final_decision == 2:
        diff = ev_auto - ns_auto
        reason = f"OPTIMIZARE FLUX: Trafic E-V ({ev_auto}) > N-S ({ns_auto})."
        decision_label = "VERDE EST-VEST"
        bg_color = "#5cb85c"
    else:
        reason = "STARE ECHILIBRU / URGENTA PREZISA DE AI"
        decision_label = "ROSU / ASTEPTARE"
        bg_color = "#d9534f"

# Scriem in log doar daca e ceva important sau random pentru demo
if random.random() < 0.3 or sirena or final_decision == -1: 
    log_decision(decision_label, reason, sirena, confidenta)

# Salvam in istoric (tratram -1 ca 0 pentru grafic)
st.session_state.history.append(final_decision if final_decision != -1 else 0)
if len(st.session_state.history) > 30: st.session_state.history.pop(0)

# Coloana dreapta: Vizualizare
with col2:
    st.subheader("🗺️ Digital Twin (Vizualizare 2D)")
    
    # Setam culorile pentru intersectie
    c_ns = "light-red"
    c_ev = "light-red"
    
    if final_decision == 1: c_ns = "light-green"
    if final_decision == 2: c_ev = "light-green"
    if final_decision == -1: # Galben Intermitent
        c_ns = "light-yellow"
        c_ev = "light-yellow"
    
    # Construim HTML-ul pentru intersectie
    html_twin = f"""
    <div class="intersection-container">
        <div></div> <div class="road {c_ns}">NORD</div> <div></div>
        <div class="road {c_ev}">VEST</div> <div class="road center">INTER</div> <div class="road {c_ev}">EST</div>
        <div></div> <div class="road {c_ns}">SUD</div> <div></div>
    </div>
    """
    st.markdown(html_twin, unsafe_allow_html=True)
    
    # Afisam decizia finala cu culoarea dinamica
    st.markdown(f'<div class="decision-box" style="background-color: {bg_color};">{decision_label}</div>', unsafe_allow_html=True)

    # Explicatia logica (textul albastru)
    st.markdown(f'<div class="xai-box"><b>LOGICA SISTEM:</b><br>{reason}</div>', unsafe_allow_html=True)
    
    # Graficul de incredere (Nou Etapa 6)
    st.write(f"**Incredere AI:** {confidenta:.2f}%")
    st.progress(int(confidenta))

# Calcul statistici pentru dashboard
if final_decision == 1: st.session_state.total_cars += ns_auto
if final_decision == 2: st.session_state.total_cars += ev_auto

# Grafic cu istoricul deciziilor
st.divider()
st.subheader("📈 Evolutia deciziilor in timp real")
st.line_chart(st.session_state.history)

st.caption(f"ℹ️ Audit activat: 'blackbox.log'. Total masini procesate: {st.session_state.total_cars}")

# Loop pentru simulare
if mode == "Auto-Play" and run_sim:
    time.sleep(refresh_speed)
    st.rerun()