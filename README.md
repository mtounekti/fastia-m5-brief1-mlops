# M5 Brief 1 – Architecture MLOps avec CI/CD
### Template modulaire déployable

---

## Description

FastIA met en place une architecture de base pour ses projets IA
Ce template modulaire et reproductible combine un frontend utilisateur,
une API REST + une conteneurisation Docker et une automatisation CI/CD via GitHub Actions

---

## Structure du projet

```
fastia-m5-brief1-mlops/
├── frontend/
│   ├── app.py              # Interface Streamlit+ Loguru
│   ├── Dockerfile
│   └── requirements.txt
├── backend/
│   ├── main.py             # API FastAPI
│   ├── modules/
│   │   ├── __init__.py
│   │   └── calcul.py       # Logique métier découplée
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_calcul.py  # 9 tests pytest
│   ├── Dockerfile
│   └── requirements.txt
├── .github/
│   └── workflows/
│       └── test.yml        # CI/CD GitHub Actions
├── docker-compose.yml
└── README.md
```

---

## stack technique

| Composant | Technologie | Rôle |
|---|---|---|
| Frontend | Streamlit | Interface utilisateur |
| Backend | FastAPI + Pydantic | API REST |
| Calcul | `modules/calcul.py` | Logique métier découplée |
| Logs | Loguru | Traçabilité frontend + backend |
| Tests | pytest | 9 cas de test |
| CI/CD | GitHub Actions | Tests automatisés sur push/PR |
| Deploy | Docker Compose | Environnement isolé et reproductible |

---

## API FastAPI

Documentation Swagger : **http://localhost:8000/docs**

| Route | Méthode | Description | Réponse |
|---|---|---|---|
| `/` | GET | Accueil de l'API | Message de bienvenue |
| `/health` | GET | Santé de l'API | `{"status": "ok"}` |
| `/calcul` | POST | Carré d'un entier | `{"nombre": 7, "resultat": 49, "operation": "7² = 49"}` |

### Exemple de requête

```bash
curl -X POST http://localhost:8000/calcul \
  -H "Content-Type: application/json" \
  -d '{"nombre": 7}'
```

### exemple de réponse

```json
{
  "nombre": 7,
  "resultat": 49,
  "operation": "7² = 49"
}
```

---

## tests pytest

9 cas de test couvrant la fonction `calcul_carre()` :

```bash
cd backend
pytest tests/ -v
```

| Test | Description |
|---|---|
| `test_carre_positif` | Entiers positifs standards |
| `test_carre_zero` | Cas limite zéro |
| `test_carre_negatif` | Entiers négatifs |
| `test_carre_grand_nombre` | Valeur maximale (10 000) |
| `test_carre_un` | Valeurs 1 et -1 |
| `test_type_float` | Float → TypeError |
| `test_type_string` | String → TypeError |
| `test_valeur_trop_grande` | > 10 000 → ValueError |
| `test_valeur_trop_petite` | < -10 000 → ValueError |

---

## CI/CD – GitHub Actions

le workflow `.github/workflows/test.yml` se déclenche automatiquement à chaque :
- **Push** sur `main`
- **Pull Request** vers `main`

il installe les dépendances et lance `pytest` sur le backend
les résultats sont visibles dans l'onglet **Actions** du repo GitHub.

---

## 🐳 déploiement Docker

```bash
# Build et lancement
docker-compose up --build

# Arrêt
docker-compose down
```

| Service | URL |
|---|---|
| Frontend (Streamlit) | http://localhost:8501 |
| Backend (FastAPI) | http://localhost:8000 |
| Documentation Swagger | http://localhost:8000/docs |

---

## installation locale (sans Docker)

```bash
git clone https://github.com/mtounekti/fastia-m5-brief1-mlops.git
cd fastia-m5-brief1-mlops

cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

cd frontend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
API_URL=http://localhost:8000 streamlit run app.py

cd backend
pytest tests/ -v
```

---

## Choix techniques justifiés

- **Logique découplée dans `modules/calcul.py`** → testable indépendamment, réutilisable
- **Pydantic** → validation automatique du type entier avant tout calcul
- **Loguru** → logs lisibles avec rotation automatique (1MB, 7 jours)
- **`depends_on` Docker Compose** → le frontend attend que le backend soit prêt
- **`healthcheck` Docker** → surveillance automatique de l'état du backend

---

<img width="1506" height="884" alt="image" src="https://github.com/user-attachments/assets/0a5597f3-0726-4624-a239-95949404f3c9" />

---

*Brief M5 – Architecture MLOps CI/CD*
