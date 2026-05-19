# =============================================================================
# backend/main.py
# API FastAPI – Template MLOps FastIA
# =============================================================================
# Routes :
#   GET  /          → Accueil
#   GET  /health    → Santé de l'API
#   POST /calcul    → Retourne le carré d'un entier
# =============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from loguru import logger
import sys
import os

# Ajout du répertoire parent pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from modules.calcul import calcul_carre

# ── Configuration Loguru ──────────────────────────────────────────────────────
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
    level="INFO"
)
logger.add(
    "logs/backend.log",
    rotation="1 MB",
    retention="7 days",
    level="DEBUG"
)

# ── Application FastAPI ────────────────────────────────────────────────────────
app = FastAPI(
    title       = "FastIA – API Template MLOps",
    description = "Template d'architecture modulaire FastIA : calcul du carré d'un entier.",
    version     = "1.0.0",
)


# ── Schémas Pydantic ──────────────────────────────────────────────────────────
class RequeteCalcul(BaseModel):
    nombre: int = Field(..., description="Entier à élever au carré", ge=-10000, le=10000)

    @validator("nombre")
    def valider_nombre(cls, v):
        if not isinstance(v, int):
            raise ValueError("Le champ 'nombre' doit être un entier")
        return v

    class Config:
        json_schema_extra = {"example": {"nombre": 7}}


class ReponseCalcul(BaseModel):
    nombre:   int
    resultat: int
    operation: str


# ── Routes ─────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Accueil"], summary="Accueil de l'API")
def accueil():
    """Route d'accueil – vérifie que l'API est opérationnelle."""
    logger.info("Route / appelée")
    return {
        "message": "Bienvenue sur l'API FastIA MLOps Template 🚀",
        "version": "1.0.0",
        "routes":  ["GET /", "GET /health", "POST /calcul"],
        "docs":    "/docs",
    }


@app.get("/health", tags=["Santé"], summary="Santé de l'API")
def health():
    """Vérifie que l'API est opérationnelle – utilisé par Docker et le monitoring."""
    logger.info("Route /health appelée")
    return {"status": "ok", "service": "backend"}


@app.post("/calcul", response_model=ReponseCalcul,
          tags=["Calcul"], summary="Calcule le carré d'un entier")
def calcul(requete: RequeteCalcul):
    """
    Reçoit un entier et retourne son carré.
    La validation du type est assurée par Pydantic.
    Le calcul est effectué dans modules/calcul.py.
    """
    logger.info(f"Route /calcul appelée avec nombre={requete.nombre}")

    try:
        resultat = calcul_carre(requete.nombre)
        logger.success(f"Calcul réussi : {requete.nombre}² = {resultat}")

        return ReponseCalcul(
            nombre    = requete.nombre,
            resultat  = resultat,
            operation = f"{requete.nombre}² = {resultat}"
        )

    except (TypeError, ValueError) as e:
        logger.error(f"Erreur de calcul : {e}")
        raise HTTPException(status_code=422, detail=str(e))