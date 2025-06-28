import streamlit as st

# Seuils critiques
TEMP_MAX = 75.0
TENSION_MIN = 200.0
COURANT_MAX = 15.0

# Puissances nominales (en MW)
PUISSANCE_SOL_NOM = 3.0
PUISSANCE_EOL_NOM = 10.0

def diagnostiquer(nom, temperature, tension, courant, puissance_actuelle, puissance_nominale):
    st.subheader(f"🔍 Diagnostic pour {nom}")
    
    if temperature > TEMP_MAX:
        st.error(f"🚨 Surchauffe détectée (Temp: {temperature} °C)")
    else:
        st.success("✅ Température normale.")

    if tension < TENSION_MIN:
        st.error(f"⚡ Tension insuffisante ({tension} V)")
    else:
        st.success("✅ Tension normale.")

    if courant > COURANT_MAX:
        st.error(f"⚠️ Surcharge de courant ({courant} A)")
    else:
        st.success("✅ Courant normal.")

    rendement = (puissance_actuelle / puissance_nominale) * 100
    if rendement < 80.0:
        st.warning(f"📉 Production faible : {puissance_actuelle} MW ({rendement:.2f}% du nominal)")
    else:
        st.success(f"🔋 Production normale : {puissance_actuelle} MW ({rendement:.2f}%)")

# Interface utilisateur
st.title("🧪 Diagnostic d'Équipements Énergétiques")

# Onglets pour chaque équipement
tab1, tab2 = st.tabs(["🌀 Éolienne", "☀️ Panneau Solaire"])

with tab1:
    st.header("🌀 Données Éolienne")
    temp_eol = st.number_input("Température (°C)", 0.0, 150.0, 60.0)
    tension_eol = st.number_input("Tension (V)", 0.0, 500.0, 220.0)
    courant_eol = st.number_input("Courant (A)", 0.0, 50.0, 12.0)
    puissance_eol = st.number_input("Puissance actuelle (MW)", 0.0, 20.0, 8.0)
    
    if st.button("Diagnostiquer l'Éolienne"):
        diagnostiquer("Éolienne", temp_eol, tension_eol, courant_eol, puissance_eol, PUISSANCE_EOL_NOM)

with tab2:
    st.header("☀️ Données Panneau Solaire")
    temp_sol = st.number_input("Température (°C)", 0.0, 150.0, 50.0, key="temp_sol")
    tension_sol = st.number_input("Tension (V)", 0.0, 500.0, 210.0, key="tension_sol")
    courant_sol = st.number_input("Courant (A)", 0.0, 50.0, 9.0, key="courant_sol")
    puissance_sol = st.number_input("Puissance actuelle (MW)", 0.0, 10.0, 2.5, key="puissance_sol")

    if st.button("Diagnostiquer le Panneau Solaire"):
        diagnostiquer("Panneau Solaire", temp_sol, tension_sol, courant_sol, puissance_sol, PUISSANCE_SOL_NOM)
