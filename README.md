# 📖 FootySim Backend

## ⚽ Description

**FootySim Backend** est une API REST construite avec **FastAPI** et **SQLAlchemy (async)** pour simuler un championnat de football.  
Elle fournit des endpoints pour gérer les saisons, clubs, joueurs, matchs, ainsi que pour générer le calendrier et calculer le classement.

C’est la partie **backend** du projet FootySim, qui repose sur une librairie interne `footysim` pour la logique métier.

---

## 🚀 Fonctionnalités

- Création et gestion des saisons
- Génération de calendrier (fixtures)
- Simulation de matchs (score, buteurs)
- Classement dynamique (table)
- Endpoints REST avec documentation auto (`/docs`)
- Compatible **SQLite** (dev) et **MySQL/Postgres** (prod)

---

## 📂 Structure du projet

```
src/app/
│── api/v1/           # Routes FastAPI (matches, players, seasons, table)
│── core/             # Configuration, connexion DB, dépendances
│── services/         # Services spécifiques backend
│── main.py           # Point d’entrée FastAPI
alembic/              # Migrations DB
venv/                 # Environnement virtuel local (non versionné)
```

---

## ⚙️ Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/ton-compte/FootySim-backend.git
cd FootySim-backend
```

### 2. Créer et activer un environnement virtuel
```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données

Créer un fichier `.env` à la racine :

#### SQLite (par défaut)
```
DATABASE_URL=sqlite+aiosqlite:///./footysim.db
```

#### MySQL
```
DATABASE_URL=mysql+aiomysql://user:password@127.0.0.1:3306/footysim
```

#### PostgreSQL
```
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/footysim
```

### 5. Créer les tables
```bash
python tun_py.py
```

ou avec Alembic (si configuré) :
```bash
alembic upgrade head
```

### 6. Lancer le serveur
```bash
uvicorn app.main:app --reload
```

Accéder à l’API :  
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🎮 Endpoints principaux

- `POST /api/v1/seasons/{id}/schedule` → Générer le calendrier
- `POST /api/v1/seasons/{id}/simulate` → Simuler une saison
- `GET /api/v1/matches/{id}` → Récupérer un match
- `GET /api/v1/table/{season_id}` → Classement de la saison

---

## 🧪 Tests

Lancer les tests unitaires :
```bash
pytest -v
```

---

## 🛠️ Roadmap

- ✅ Classement API (`/table/{season_id}`)
- 🚧 Endpoint top buteurs
- 🚧 Gestion des transferts
- 🚧 Statistiques avancées
- 🚧 Intégration CI/CD

---

## 📜 Licence

Projet pédagogique — librement réutilisable et modifiable.  
