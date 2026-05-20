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

# M5 Brief 2 – CD automatisé vers Docker Hub
### Pipeline CI/CD complet

---

## Description

Extension du Brief 1 avec un pipeline de **déploiement continu (CD)**
À chaque push sur `main` les images Docker sont automatiquement
buildées, taguées et publiées sur Docker Hub via GitHub Actions

---

## Pipeline CI/CD complet

```
git push → main
    │
    ├── test.yml        → pytest (CI)  ✅
    │
    └── docker-publish.yml → Build + Push Docker Hub (CD) ✅
```

---

## 🐳 Images Docker Hub

| Image | Lien |
|---|---|
| Backend | [mtounekti/fastia-backend](https://hub.docker.com/r/mtounekti/fastia-backend) |
| Frontend | [mtounekti/fastia-frontend](https://hub.docker.com/r/mtounekti/fastia-frontend) |

### Pull et run depuis Docker Hub

```bash
# pull les images
docker pull mtounekti/fastia-backend:latest
docker pull mtounekti/fastia-frontend:latest

docker run -p 8000:8000 mtounekti/fastia-backend:latest

docker run -p 8501:8501 -e API_URL=http://localhost:8000 \
  mtounekti/fastia-frontend:latest
```

### Tags disponibles

| Tag | Description |
|---|---|
| `latest` | Dernière version stable |
| `<github.sha>` | Hash du commit exact pour traçabilité |

---

## Workflow CD – docker-publish.yml

Déclenché à chaque **push sur `main`** :

1. 📥 Checkout du code
2. 🐳 Setup Docker Buildx
3. 🔐 Login Docker Hub (via secrets GitHub)
4. 💾 Cache Docker layers (optimisation des builds)
5. 🔨 Build & Push image Backend (`latest` + `sha`)
6. 🔨 Build & Push image Frontend (`latest` + `sha`)
7. 🔄 Rotation du cache

---

## Secrets GitHub configurés

| Secret | Valeur |
|---|---|
| `DOCKER_USERNAME` | `mtounekti` |
| `DOCKER_PASSWORD` | Token Docker Hub (jamais exposé) |

---

## Variables d'environnement

Voir `.env.example` pour la configuration :

```bash
APP_VERSION=1.0.0
DOCKER_USERNAME=mtounekti
IMAGE_BACKEND=mtounekti/fastia-backend
IMAGE_FRONTEND=mtounekti/fastia-frontend
```

---

## Lancement complet depuis Docker Hub

```bash
# sans cloner le repo – directement depuis Docker Hub
docker run -d -p 8000:8000 mtounekti/fastia-backend:latest
docker run -d -p 8501:8501 -e API_URL=http://localhost:8000 \
  mtounekti/fastia-frontend:latest
```

Ou avec docker-compose (après avoir cloné le repo) :

```bash
docker-compose up
```

---

## Fichiers ajoutés dans ce brief

```
fastia-m5-brief1-mlops/
├── .github/
│   └── workflows/
│       ├── test.yml             # CI – pytest (Brief 1)
│       └── docker-publish.yml  # CD – Docker Hub (Brief 2)
├── .env.example                 # Template de configuration
└── README.md
```

---

*Brief M5 – Architecture MLOps CI/CD + CD Docker Hub*
