[README.md](https://github.com/user-attachments/files/32335260/README.md)
# JobConnect

> Plateforme de mise en relation entre **candidats** et **recruteurs**  
> Stack : **Django 6.1 + DRF + WebSocket** (backend) · **React 19 + Vite + TailwindCSS** (frontend)

---

## 📋 Résumé du projet

**JobConnect** est une application full-stack permettant :

| Rôle | Fonctionnalités |
|---|---|
| **Candidat** | Créer un profil (CV, photo, LinkedIn/GitHub), rechercher des offres, postuler, mettre en favoris, chatter avec les recruteurs |
| **Recruteur** | Publier/gérer des offres d'emploi, consulter les candidatures reçues, chatter avec les candidats |
| **Admin** | Superviser la plateforme via un tableau de bord dédié (statistiques globales) |

La messagerie est **temps réel** via WebSocket (Django Channels + Redis).

---

## 🏗️ Architecture globale

```
Jobconnect/
├── jobconnect-backend/    ← API Django REST + WebSocket
└── jobconnect-frontend/   ← SPA React + Vite
```

```
┌─────────────────────────────────────────────────────┐
│              Frontend (React 19 / Vite)              │
│         localhost:5173  ·  TailwindCSS 4             │
└──────────────┬──────────────────────────┬───────────┘
               │ HTTP/REST (Axios)        │ WebSocket
               ▼                          ▼
┌─────────────────────────────────────────────────────┐
│               Backend (Daphne / ASGI)               │
│  ┌─────────────────────┐  ┌───────────────────────┐ │
│  │  Django REST Frame  │  │   Django Channels     │ │
│  │  work (ViewSets,    │  │   ChatConsumer (WS)   │ │
│  │  Serializers, JWT)  │  │   JWTAuthMiddleware   │ │
│  └──────────┬──────────┘  └──────────┬────────────┘ │
└─────────────┼───────────────────────┼───────────────┘
              ▼                        ▼
   ┌──────────────────┐    ┌───────────────────────┐
   │   PostgreSQL     │    │        Redis           │
   │   (données)      │    │  (Channel Layers WS)   │
   └──────────────────┘    └───────────────────────┘
```

---

## 🔧 Backend — `jobconnect-backend/`

### Structure

```
jobconnect-backend/
├── config/
│   ├── settings.py       # DB, JWT, Redis, CORS, pagination…
│   ├── urls.py           # Routage principal (DefaultRouter)
│   ├── asgi.py           # ProtocolTypeRouter HTTP + WS
│   └── wsgi.py
├── apps/
│   ├── accounts/         # Auth, utilisateurs, profils
│   ├── companies/        # Fiches entreprises
│   ├── jobs/             # Offres d'emploi, compétences
│   ├── applications/     # Candidatures
│   ├── favorites/        # Favoris candidats
│   ├── messaging/        # Chat temps réel (WebSocket)
│   └── notifications/    # Notifications
├── seed/                 # Données de test
├── media/                # Upload CVs, photos
├── manage.py
└── requirements.txt
```

### Applications Django

| App | Modèles clés | Description |
|---|---|---|
| **accounts** | `User`, `CandidateProfile`, `RecruiterProfile` | Auth email, 3 rôles (CANDIDATE / RECRUITER / ADMIN), upload CV & photo, liens LinkedIn/GitHub |
| **companies** | `Company` | Fiches entreprises, liées aux recruteurs |
| **jobs** | `JobOffer`, `Skill` | Offres avec contrat (CDI/CDD/Freelance…), niveau, salaire, remote, statut (DRAFT/PUBLISHED/CLOSED), compétences M2M |
| **applications** | `Application` | Dépôt & suivi des candidatures |
| **favorites** | `FavoriteJob` | Sauvegarde d'offres par les candidats |
| **messaging** | `Conversation`, `Message` | Chat 1-to-1 persisté + diffusion WebSocket (Redis) |
| **notifications** | `Notification` | Alertes utilisateurs |

### Endpoints REST

| Méthode & URL | Description |
|---|---|
| `POST /api/accounts/login/` | Connexion (JWT) |
| `POST /api/accounts/refresh/` | Rafraîchissement token |
| `POST /api/accounts/verify/` | Vérification token |
| `GET /api/accounts/admin/dashboard/` | Tableau de bord admin |
| `GET/PATCH /api/accounts/candidates/{id}/` | Profil candidat |
| `GET/PATCH /api/accounts/recruiters/{id}/` | Profil recruteur |
| `GET/POST /api/companies/` | Entreprises |
| `GET/POST /api/jobs/` | Offres d'emploi |
| `GET/POST /api/skills/` | Compétences |
| `GET/POST /api/applications/` | Candidatures |
| `GET/POST /api/favorites/` | Favoris |
| `GET/POST /api/conversations/` | Conversations |
| `GET/POST /api/messages/` | Messages |
| `GET/PATCH /api/notifications/` | Notifications |
| `GET /api/docs/` | Swagger UI |
| `GET /api/schema/` | Schéma OpenAPI |

### WebSocket

```
ws://127.0.0.1:8000/ws/chat/<conversation_id>/
```

- Authentification via token JWT en query string
- `JWTAuthMiddleware` → `ChatConsumer` (AsyncWebsocketConsumer)
- Diffusion via Redis Channel Layer

---

## 🎨 Frontend — `jobconnect-frontend/`

### Structure

```
jobconnect-frontend/
├── src/
│   ├── App.jsx              # Routage React Router v7
│   ├── main.jsx             # Point d'entrée
│   ├── context/
│   │   └── AuthContext.jsx  # Contexte auth global (JWT + user)
│   ├── services/
│   │   ├── api.js           # Instance Axios + intercepteurs JWT (refresh auto)
│   │   └── websocket.js     # Client WebSocket
│   ├── components/
│   │   ├── layout/          # Navbar, Layout principal
│   │   └── chat/            # Composants messagerie
│   ├── pages/
│   │   ├── home/            # Page d'accueil
│   │   ├── auth/            # Login, Register
│   │   ├── jobs/            # Liste offres, Détail offre, Formulaire recruteur
│   │   ├── applications/    # Mes candidatures (candidat), Candidatures reçues (recruteur)
│   │   ├── favorites/       # Offres favorites
│   │   ├── profile/         # Profil utilisateur
│   │   ├── messaging/       # Chat
│   │   └── admin/           # Dashboard admin
│   └── i18n/                # Internationalisation (i18next)
├── index.html
├── vite.config.js
├── package.json
└── .env
```

### Pages & Routes

| Route | Page | Accès |
|---|---|---|
| `/` | Home | Public |
| `/login` | Connexion | Public |
| `/register` | Inscription | Public |
| `/jobs` | Liste des offres | Public |
| `/jobs/:id` | Détail d'une offre | Public |
| `/applications` | Mes candidatures | Candidat |
| `/favorites` | Mes favoris | Candidat |
| `/profile` | Mon profil | Connecté |
| `/chat` | Messagerie | Connecté |
| `/recruiter/jobs/new` | Créer une offre | Recruteur |
| `/recruiter/jobs/:id/edit` | Modifier une offre | Recruteur |
| `/recruiter/applications` | Candidatures reçues | Recruteur |
| `/admin` | Dashboard admin | Admin |

---

## 🛠️ Technologies utilisées

### Backend

| Technologie | Version | Rôle |
|---|---|---|
| **Python** | 3.x | Langage |
| **Django** | 6.1 | Framework web |
| **Django REST Framework** | 3.18.0 | API REST |
| **Django Channels** | 4.3.2 | WebSocket / ASGI |
| **Daphne** | 4.2.3 | Serveur ASGI |
| **djangorestframework-simplejwt** | 5.5.1 | Authentification JWT |
| **django-cors-headers** | 4.9.0 | CORS |
| **drf-spectacular** | 0.30.0 | Swagger / OpenAPI |
| **django-filter** | 26.1 | Filtrage avancé |
| **PostgreSQL** | — | Base de données |
| **psycopg** | 3.3.4 | Driver PostgreSQL async |
| **Redis** | 8.1.0 | Channel Layer WS |
| **channels-redis** | 4.3.0 | Backend Redis |
| **Pillow** | 12.3.0 | Traitement images |
| **python-dotenv** | 1.2.2 | Variables d'environnement |

### Frontend

| Technologie | Version | Rôle |
|---|---|---|
| **React** | 19.x | Framework UI |
| **Vite** | 8.x | Bundler / Dev server |
| **TailwindCSS** | 4.x | Styles utilitaires |
| **React Router DOM** | 7.x | Routage SPA |
| **Axios** | 1.x | Client HTTP + intercepteurs JWT |
| **Recharts** | 3.x | Graphiques (dashboard admin) |
| **i18next / react-i18next** | 26.x / 17.x | Internationalisation |
| **Lucide React** | 1.x | Icônes |

---

## ⚙️ Configuration

### Backend `.env`

```env
SECRET_KEY=votre-clé-secrète
DEBUG=True

# PostgreSQL
DB_NAME=jobconnect_db
DB_USER=postgres
DB_PASSWORD=motdepasse
DB_HOST=127.0.0.1
DB_PORT=5432

# Redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Frontend `.env`

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

### JWT (backend)
- **Access token** : 60 minutes
- **Refresh token** : 7 jours (rotation activée)
- **Header** : `Authorization: Bearer <token>`
- Le frontend gère le **refresh automatique** via un intercepteur Axios

---

## 🚀 Démarrage

### Backend

```bash
# 1. Environnement virtuel
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate      # Linux/Mac

# 2. Dépendances
pip install -r requirements.txt

# 3. Migrations
python manage.py migrate

# 4. (Optionnel) Données de test
python manage.py seed

# 5. Lancer le serveur ASGI
daphne config.asgi:application
# ou en développement
python manage.py runserver
```

> ⚠️ **Redis** doit être actif avant de lancer le backend (requis pour les WebSockets).

### Frontend

```bash
# 1. Dépendances
npm install

# 2. Développement
npm run dev          # → http://localhost:5173

# 3. Production
npm run build
npm run preview
```

---

## 📐 Conventions

| Paramètre | Valeur |
|---|---|
| Langue | `fr-fr` |
| Fuseau horaire | `Europe/Paris` |
| Pagination API | 20 éléments / page |
| Port backend | `8000` |
| Port frontend | `5173` |
| Formats CV acceptés | PDF, DOC, DOCX |
| Upload médias | `media/cvs/` · `media/profiles/` |
