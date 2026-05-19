import streamlit as st
import requests
from loguru import logger
import sys
import os

# conf Loguru
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
    level="INFO"
)
logger.add(
    "logs/frontend.log",
    rotation="1 MB",
    retention="7 days",
    level="DEBUG"
)

os.makedirs("logs", exist_ok=True)

# conf API
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Interface Streamlit
st.set_page_config(
    page_title = "FastIA – MLOps Template",
    page_icon  = "🚀",
    layout     = "centered"
)

st.title("🚀 FastIA – MLOps Template")
st.caption("Architecture modulaire : Streamlit + FastAPI + Docker + CI/CD")

st.divider()

# Vérification santé API
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Calculateur de carré")

with col2:
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        if response.status_code == 200:
            st.success("API ✅")
            logger.info("API en ligne")
        else:
            st.error("API ❌")
    except Exception:
        st.error("API ❌")
        logger.warning("API inaccessible")

# formulaire de calcul
with st.form("form_calcul"):
    nombre = st.number_input(
        "Entrer un entier",
        min_value = -10000,
        max_value = 10000,
        value     = 0,
        step      = 1,
        help      = "Entier entre -10 000 et 10 000"
    )
    submit = st.form_submit_button("Calculer le carré ⚡", use_container_width=True)

if submit:
    logger.info(f"Requête envoyée : nombre={nombre}")
    try:
        response = requests.post(
            f"{API_URL}/calcul",
            json    = {"nombre": int(nombre)},
            timeout = 5
        )

        if response.status_code == 200:
            data = response.json()
            st.success(f"**{data['operation']}**")
            st.metric(label="Résultat", value=data["resultat"])
            logger.success(f"Résultat reçu : {data['operation']}")

        else:
            detail = response.json().get("detail", "Erreur inconnue")
            st.error(f"Erreur : {detail}")
            logger.error(f"Erreur API : {detail}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Impossible de contacter l'API. Vérifiez que le backend est lancé.")
        logger.error("Connexion API échouée")
    except Exception as e:
        st.error(f"Erreur inattendue : {e}")
        logger.error(f"Erreur inattendue : {e}")

st.divider()

# info architecture
with st.expander("ℹ️ Architecture du projet"):
    st.markdown("""
    | Composant | Technologie | Rôle |
    |---|---|---|
    | Frontend | Streamlit | Interface utilisateur |
    | Backend | FastAPI | API REST (3 routes) |
    | Calcul | modules/calcul.py | Logique métier découplée |
    | Logs | Loguru | Traçabilité |
    | Tests | pytest | Couverture de code |
    | CI/CD | GitHub Actions | Tests automatisés |
    | Deploy | Docker Compose | Environnement isolé |
    """)