import streamlit as st
import math
import random
import time

# --- Global Configuration and Page Setup ---
st.set_page_config(layout="wide", page_title="Système Hybride Éolien-Solaire")

st.title("⚡ Système Hybride Éolien-Solaire : Gestion Optimisée")
st.markdown("Cette application simule et aide à la gestion d'un système énergétique hybride.")

# --- Section 1: Diagnostic des Pannes Functions ---
# Seuils critiques
TEMP_MAX = 75.0
TENSION_MIN = 200.0
COURANT_MAX = 15.0

# Puissances nominales (en MW)
PUISSANCE_SOL_NOM = 3.0
PUISSANCE_EOL_NOM = 10.0

def diagnostiquer(nom, temperature, tension, courant, puissance_actuelle, puissance_nominale):
    """
    Fonction de diagnostic des pannes.
    Affiche le statut de l'équipement en fonction de ses paramètres.
    """
    st.subheader(f"🔍 Diagnostic pour **{nom}**")
    st.markdown("---")

    if temperature > TEMP_MAX:
        st.error(f"🚨 **Surchauffe détectée** : Température actuelle: {temperature}°C (Seuil: {TEMP_MAX}°C)")
    else:
        st.success(f"✅ **Température normale** : {temperature}°C")

    if tension < TENSION_MIN:
        st.error(f"⚡ **Tension insuffisante** : Tension actuelle: {tension} V (Seuil: {TENSION_MIN} V)")
    else:
        st.success(f"✅ **Tension normale** : {tension} V")

    if courant > COURANT_MAX:
        st.error(f"⚠️ **Surcharge de courant** : Courant actuel: {courant} A (Seuil: {COURANT_MAX} A)")
    else:
        st.success(f"✅ **Courant normal** : {courant} A")

    if puissance_nominale > 0:
        rendement = (puissance_actuelle / puissance_nominale) * 100
        if rendement < 80.0:
            st.warning(f"📉 **Production faible** : {puissance_actuelle} MW ({rendement:.2f}% du nominal {puissance_nominale} MW)")
        else:
            st.success(f"🔋 **Production normale** : {puissance_actuelle} MW ({rendement:.2f}%)")
    else:
        st.info("ℹ️ Puissance nominale non définie pour le calcul du rendement.")

# --- Section 2: Maintenance Functions ---
# Paramètres de maintenance
MAX_OPERATING_HOURS_WIND = 1000
MAX_OPERATING_HOURS_SOLAR = 1500

# Variables d'état pour la maintenance
if 'wind_operating_hours' not in st.session_state:
    st.session_state.wind_operating_hours = 0
if 'solar_operating_hours' not in st.session_state:
    st.session_state.solar_operating_hours = 0
if 'maintenance_log' not in st.session_state:
    st.session_state.maintenance_log = []

def perform_wind_maintenance():
    """Effectue la maintenance de l'éolienne et réinitialise les heures de fonctionnement."""
    st.session_state.wind_operating_hours = 0
    log_entry = f"⚙️ Maintenance de l'éolienne effectuée le {time.strftime('%Y-%m-%d %H:%M:%S')}."
    st.session_state.maintenance_log.append(log_entry)
    st.info(log_entry)

def perform_solar_maintenance():
    """Effectue la maintenance du panneau solaire et réinitialise les heures de fonctionnement."""
    st.session_state.solar_operating_hours = 0
    log_entry = f"⚙️ Maintenance du panneau solaire effectuée le {time.strftime('%Y-%m-%d %H:%M:%S')}."
    st.session_state.maintenance_log.append(log_entry)
    st.info(log_entry)

def update_system_maintenance(hours_passed_wind, hours_passed_solar):
    """
    Met à jour les heures de fonctionnement et vérifie la nécessité de maintenance.
    """
    st.session_state.wind_operating_hours += hours_passed_wind
    st.session_state.solar_operating_hours += hours_passed_solar

    needs_wind_maintenance = False
    needs_solar_maintenance = False

    if st.session_state.wind_operating_hours >= MAX_OPERATING_HOURS_WIND:
        needs_wind_maintenance = True
    if st.session_state.solar_operating_hours >= MAX_OPERATING_HOURS_SOLAR:
        needs_solar_maintenance = True

    return needs_wind_maintenance, needs_solar_maintenance

# --- Section 3: Stabilité sur le Réseau Électrique Functions ---
DEMANDE_FIXE = 11.5 # MW
FREQ_NOMINALE = 50.0 # Hz
TENSION_NOMINALE = 230.0 # V

def production_eolienne_sim(h):
    """Simule la production éolienne en fonction de l'heure."""
    vent = 5 + 5 * math.sin(h * math.pi / 12)
    return min(10.0, max(0.0, vent))

def production_solaire_sim(h):
    """Simule la production solaire en fonction de l'heure."""
    if 6 <= h <= 18:
        return 3 * math.sin((h - 6) * math.pi / 12)
    return 0.0

def ajuster_frequence(production, demande):
    """Ajuste la fréquence du réseau en fonction de l'écart production-demande."""
    delta_p = production - demande
    return FREQ_NOMINALE + delta_p * 0.2

def ajuster_tension(production, demande):
    """Ajuste la tension du réseau en fonction de la variation de puissance."""
    if demande == 0: return TENSION_NOMINALE
    delta = (production - demande) / demande
    return TENSION_NOMINALE * (1 + delta * 0.1)

def est_stable(freq, tension):
    """Vérifie si le système est stable."""
    return (freq >= 49.5 and freq <= 50.5) and \
           (tension >= 0.95 * TENSION_NOMINALE and tension <= 1.05 * TENSION_NOMINALE)

# --- Section 4: Algorithme de Contrôle Functions ---
# Paramètres du système de contrôle
SEUIL_CHARGE_BATTERIE_MIN = 20.0
SEUIL_DECHARGE_BATTERIE_MAX = 80.0

# Variables d'état pour l'algorithme de contrôle
if 'prod_solaire_ctrl' not in st.session_state:
    st.session_state.prod_solaire_ctrl = 200.0
if 'prod_eolienne_ctrl' not in st.session_state:
    st.session_state.prod_eolienne_ctrl = 150.0
if 'demande_charge_ctrl' not in st.session_state:
    st.session_state.demande_charge_ctrl = 300.0
if 'etat_charge_batterie_ctrl' not in st.session_state:
    st.session_state.etat_charge_batterie_ctrl = 50.0

def lire_sources():
    """Simule la lecture de production (avec une légère variation aléatoire)."""
    st.session_state.prod_solaire_ctrl = 200.0 + (random.random() * 100 - 50)
    st.session_state.prod_eolienne_ctrl = 150.0 + (random.random() * 50 - 25)

def lire_demande_charge():
    """Simule la lecture de la demande de charge (avec une légère variation aléatoire)."""
    st.session_state.demande_charge_ctrl = 300.0 + (random.random() * 50 - 25)

def optimiser_energie():
    """
    Fonction de contrôle de la production et de l'utilisation de l'énergie.
    """
    production_totale = st.session_state.prod_solaire_ctrl + st.session_state.prod_eolienne_ctrl
    log_messages = []

    if production_totale > st.session_state.demande_charge_ctrl:
        excedent = production_totale - st.session_state.demande_charge_ctrl
        if st.session_state.etat_charge_batterie_ctrl < SEUIL_DECHARGE_BATTERIE_MAX:
            st.session_state.etat_charge_batterie_ctrl += excedent * 0.005
            if st.session_state.etat_charge_batterie_ctrl > 100.0:
                st.session_state.etat_charge_batterie_ctrl = 100.0
            log_messages.append(f"🟢 Excédent stocké dans la batterie. SOC : {st.session_state.etat_charge_batterie_ctrl:.2f}%")
        else:
            log_messages.append("🟡 Production réduite pour éviter la surcharge de la batterie (batterie pleine).")
    elif st.session_state.demande_charge_ctrl > production_totale:
        deficit = st.session_state.demande_charge_ctrl - production_totale
        if st.session_state.etat_charge_batterie_ctrl > SEUIL_CHARGE_BATTERIE_MIN:
            st.session_state.etat_charge_batterie_ctrl -= deficit * 0.005
            if st.session_state.etat_charge_batterie_ctrl < 0.0:
                st.session_state.etat_charge_batterie_ctrl = 0.0
            log_messages.append(f"🔴 Déficit comblé par la batterie. SOC : {st.session_state.etat_charge_batterie_ctrl:.2f}%")
        else:
            log_messages.append("❌ Déficit non comblé, réduction de consommation nécessaire (batterie faible).")
    else:
        log_messages.append("🔵 Production équilibrée avec la demande.")

    return log_messages

# --- Sidebar Navigation ---
with st.sidebar:
    st.header("Navigation Principale")
    page_selection = st.radio(
        "Sélectionnez une section :",
        [
            "🛠️ Diagnostic des Pannes",
            "⚙️ Simulation de Maintenance",
            "📈 Stabilité sur le Réseau",
            "🧠 Algorithme de Contrôle"
        ],
        key="main_navigation_radio"
    )
    st.markdown("---")
    st.write("Conçu pour un système hybride éolien-solaire.")


# --- Content Display based on Sidebar Selection ---

if page_selection == "🛠️ Diagnostic des Pannes":
    st.header("🛠️ Diagnostic des Pannes")
    st.write("Entrez les paramètres actuels de l'équipement pour diagnostiquer d'éventuelles pannes.")

    st.subheader("🌀 Données Éolienne")
    temp_eol = st.slider("Température Éolienne (°C)", 0.0, 150.0, 60.0, step=0.1, key="temp_eol_diag")
    tension_eol = st.slider("Tension Éolienne (V)", 0.0, 500.0, 220.0, step=1.0, key="tension_eol_diag")
    courant_eol = st.slider("Courant Éolienne (A)", 0.0, 50.0, 12.0, step=0.1, key="courant_eol_diag")
    puissance_eol = st.slider("Puissance actuelle Éolienne (MW)", 0.0, 20.0, 7.5, step=0.1, key="puissance_eol_diag")

    if st.button("Diagnostiquer l'Éolienne", key="btn_diag_eol"):
        diagnostiquer("Éolienne", temp_eol, tension_eol, courant_eol, puissance_eol, PUISSANCE_EOL_NOM)

    st.markdown("---")

    st.subheader("☀️ Données Panneau Solaire")
    temp_sol = st.slider("Température Panneau Solaire (°C)", 0.0, 150.0, 50.0, step=0.1, key="temp_sol_diag")
    tension_sol = st.slider("Tension Panneau Solaire (V)", 0.0, 500.0, 210.0, step=1.0, key="tension_sol_diag")
    courant_sol = st.slider("Courant Panneau Solaire (A)", 0.0, 50.0, 9.0, step=0.1, key="courant_sol_diag")
    puissance_sol = st.slider("Puissance actuelle Panneau Solaire (MW)", 0.0, 10.0, 2.2, step=0.1, key="puissance_sol_diag")

    if st.button("Diagnostiquer le Panneau Solaire", key="btn_diag_sol"):
        diagnostiquer("Panneau Solaire", temp_sol, tension_sol, courant_sol, puissance_sol, PUISSANCE_SOL_NOM)

elif page_selection == "⚙️ Simulation de Maintenance":
    st.header("⚙️ Simulation de Maintenance")
    st.write("Simulez le fonctionnement du système et l'exécution des maintenances préventives.")

    st.markdown(f"**Éolienne** : Maintenance requise après **{MAX_OPERATING_HOURS_WIND} heures** de fonctionnement.")
    st.markdown(f"**Panneau Solaire** : Maintenance requise après **{MAX_OPERATING_HOURS_SOLAR} heures** de fonctionnement.")

    col_wind_metrics, col_solar_metrics = st.columns(2)
    with col_wind_metrics:
        st.metric("Heures de fonctionnement Éolienne", f"{st.session_state.wind_operating_hours} / {MAX_OPERATING_HOURS_WIND} heures")
    with col_solar_metrics:
        st.metric("Heures de fonctionnement Panneau Solaire", f"{st.session_state.solar_operating_hours} / {MAX_OPERATING_HOURS_SOLAR} heures")

    st.subheader("Ajouter des heures de fonctionnement")
    hours_to_add_wind = st.slider("Heures à ajouter à l'Éolienne", 0, 200, 24, key="add_wind_hours")
    if st.button("Simuler heures Éolienne", key="sim_wind_hours_btn"):
        needs_w, needs_s = update_system_maintenance(hours_to_add_wind, 0)
        if needs_w:
            st.warning(f"L'éolienne a dépassé {MAX_OPERATING_HOURS_WIND} heures et nécessite une maintenance.")
        st.rerun()

    hours_to_add_solar = st.slider("Heures à ajouter au Panneau Solaire", 0, 200, 24, key="add_solar_hours")
    if st.button("Simuler heures Panneau Solaire", key="sim_solar_hours_btn"):
        needs_w, needs_s = update_system_maintenance(0, hours_to_add_solar)
        if needs_s:
            st.warning(f"Le panneau solaire a dépassé {MAX_OPERATING_HOURS_SOLAR} heures et nécessite une maintenance.")
        st.rerun()

    if st.session_state.wind_operating_hours >= MAX_OPERATING_HOURS_WIND:
        if st.button("Effectuer Maintenance Éolienne", key="do_wind_maint"):
            perform_wind_maintenance()
            st.rerun()

    if st.session_state.solar_operating_hours >= MAX_OPERATING_HOURS_SOLAR:
        if st.button("Effectuer Maintenance Panneau Solaire", key="do_solar_maint"):
            perform_solar_maintenance()
            st.rerun()

    st.markdown("---")
    st.subheader("Historique des Maintenances")
    if st.session_state.maintenance_log:
        for entry in reversed(st.session_state.maintenance_log):
            st.text(entry)
    else:
        st.info("Aucune maintenance effectuée pour l'instant.")

    if st.button("Réinitialiser toutes les heures de fonctionnement et log", key="reset_maintenance"):
        st.session_state.wind_operating_hours = 0
        st.session_state.solar_operating_hours = 0
        st.session_state.maintenance_log = []
        st.success("Heures de fonctionnement et log de maintenance réinitialisés.")
        st.rerun()

elif page_selection == "📈 Stabilité sur le Réseau":
    import pandas as pd # Import pandas here as it's only used in this section
    st.header("📈 Stabilité sur le Réseau Électrique")
    st.write("Visualisez la production d'énergie, la fréquence et la tension du réseau sur une journée, et évaluez sa stabilité.")

    heures = list(range(24))
    productions_eol = [production_eolienne_sim(h) for h in heures]
    productions_sol = [production_solaire_sim(h) for h in heures]
    productions_tot = [pe + ps for pe, ps in zip(productions_eol, productions_sol)]

    frequences = [ajuster_frequence(pt, DEMANDE_FIXE) for pt in productions_tot]
    tensions = [ajuster_tension(pt, DEMANDE_FIXE) for pt in productions_tot]
    stab_status = [est_stable(f, t) for f, t in zip(frequences, tensions)]

    data_stability = pd.DataFrame({
        "Heure": heures,
        "Prod. Éolienne (MW)": productions_eol,
        "Prod. Solaire (MW)": productions_sol,
        "Prod. Totale (MW)": productions_tot,
        "Demande (MW)": [DEMANDE_FIXE] * 24,
        "Fréquence (Hz)": frequences,
        "Tension (V)": tensions,
        "Stabilité": ["Stable" if s else "Instable" for s in stab_status]
    })

    st.dataframe(data_stability) # st.dataframe handles horizontal scrolling well on mobile

    st.line_chart(data_stability, x="Heure", y=["Prod. Totale (MW)", "Demande (MW)"])
    st.line_chart(data_stability, x="Heure", y=["Fréquence (Hz)", "Tension (V)"])

    instabilities = data_stability[data_stability["Stabilité"] == "Instable"]
    if not instabilities.empty:
        st.warning("⚠️ **Périodes d'instabilité détectées !**")
        st.table(instabilities[["Heure", "Fréquence (Hz)", "Tension (V)", "Stabilité"]])
    else:
        st.success("✅ Le système semble stable sur toute la période simulée.")

elif page_selection == "🧠 Algorithme de Contrôle":
    st.header("🧠 Algorithme de Contrôle d'Énergie")
    st.write("Simule et optimise la gestion de l'énergie et de la batterie pour équilibrer production et demande.")

    with st.expander("Voir les seuils de batterie"):
        st.info(f"Seuil de charge batterie minimum : **{SEUIL_CHARGE_BATTERIE_MIN}%**")
        st.info(f"Seuil de décharge batterie maximum : **{SEUIL_DECHARGE_BATTERIE_MAX}%**")

    st.markdown("---")
    st.subheader("Paramètres actuels (Simulés)")

    # Columns for metrics, these will stack nicely on mobile
    col_prod_s, col_prod_e, col_demande, col_soc = st.columns(4)
    with col_prod_s:
        st.metric("Prod. Solaire (W)", f"{st.session_state.prod_solaire_ctrl:.2f}")
    with col_prod_e:
        st.metric("Prod. Éolienne (W)", f"{st.session_state.prod_eolienne_ctrl:.2f}")
    with col_demande:
        st.metric("Demande (W)", f"{st.session_state.demande_charge_ctrl:.2f}")
    with col_soc:
        st.metric("SOC Batterie", f"{st.session_state.etat_charge_batterie_ctrl:.2f}%")

    st.markdown("---")
    if st.button("Lancer une Itération de Contrôle", key="run_control_iter"):
        st.subheader("Résultats de l'itération :")
        lire_sources()
        lire_demande_charge()

        st.write(f"**Avant optimisation :**")
        st.write(f"  Production Solaire : {st.session_state.prod_solaire_ctrl:.2f} W")
        st.write(f"  Production Éolienne : {st.session_state.prod_eolienne_ctrl:.2f} W")
        st.write(f"  Demande : {st.session_state.demande_charge_ctrl:.2f} W")
        st.write(f"  SOC Batterie : {st.session_state.etat_charge_batterie_ctrl:.2f}%")

        messages = optimiser_energie()
        for msg in messages:
            st.write(msg)

        st.write(f"**Après optimisation :**")
        st.write(f"  Nouveau SOC Batterie : {st.session_state.etat_charge_batterie_ctrl:.2f}%")
        st.success("Itération terminée.")
        st.rerun()

    if st.button("Réinitialiser l'Algorithme de Contrôle", key="reset_control_algo"):
        st.session_state.prod_solaire_ctrl = 200.0
        st.session_state.prod_eolienne_ctrl = 150.0
        st.session_state.demande_charge_ctrl = 300.0
        st.session_state.etat_charge_batterie_ctrl = 50.0
        st.success("Algorithme de contrôle réinitialisé.")
        st.rerun()