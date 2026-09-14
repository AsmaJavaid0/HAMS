# Hospital Asset Management

[hospital-asset-management.vercel.app](https://hospital-asset-management.vercel.app/)

Yeh project hospital assets ko manage karne ke liye banaya gaya hai. Is repository mein:
- `backend/` (FastAPI + SQLAlchemy)
- `frontend/` (Nuxt 4 + Vue 3)

Is README mein backend aur frontend dono ka setup aur run process diya gaya hai.

## 1) Prerequisites

System mein yeh tools installed hon:
- Python 3.10+
- Node.js 18+ (ya latest LTS)
- npm
- PostgreSQL database (local) ya Supabase Postgres

## 2) Repository Clone

Agar project clone nahi kiya to:

```powershell
git clone <your-repo-url>
cd hospital-asset-management
```

## 3) Backend Setup (FastAPI)

### 3.1 Backend folder mein jao

```powershell
cd backend
```

### 3.2 Virtual environment banao aur activate karo

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3.3 Dependencies install karo

```powershell
pip install -r requirements.txt
```

### 3.4 `.env` file banao

`backend/.env` file create karo aur minimum yeh variables set karo:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DB_NAME
JWT_SECRET_KEY=your-very-strong-secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_SECRET_KEY=your-supabase-service-role-key
```

Notes:
- `DATABASE_URL` required hai, warna app start nahi hogi.
- `JWT_SECRET_KEY` required hai, warna auth module runtime error dega.
- `SUPABASE_URL` aur `SUPABASE_SECRET_KEY` app startup par read hotay hain.

### 3.5 Backend run karo

```powershell
uvicorn app.main:app --reload --port 8000
```

### 3.6 Backend test

Browser ya API client se check karo:
- `GET http://localhost:8000/` -> expected message: `AssetCare backend is running`

Auth routes base path:
- `/api/auth/*`

## 4) Frontend Setup (Nuxt)

Nayi terminal kholo, project root par aao, phir:

```powershell
cd frontend
npm install
npm run dev
```

Frontend default URL:
- `http://localhost:3000`

## 5) Development Run (Backend + Frontend)

Local development mein dono servers parallel run karo:
- Terminal 1: backend (`http://localhost:8000`)
- Terminal 2: frontend (`http://localhost:3000`)

## 6) Current Integration Status

Current frontend auth flow mostly demo/mock mode mein hai:
- Login page `useAuth` composable ke through mock token/user set karta hai.
- Register page par backend registration call abhi connect nahi hai.

Agar aap full API integration karna chahte hain to frontend se `/api/auth/login` aur `/api/auth/register-hospital` endpoints connect karne honge.

## 7) Helpful Commands

Backend (inside `backend/`):

```powershell
# venv activate
.\.venv\Scripts\Activate.ps1

# run server
uvicorn app.main:app --reload --port 8000
```

Frontend (inside `frontend/`):

```powershell
npm run dev
npm run build
npm run preview
```

AssetCare General Hospital
│
├── Main Hospital Building
│   ├── Ground Floor
│   │   └── Emergency Department
│   │       ├── Triage
│   │       ├── Resuscitation 1
│   │       ├── Resuscitation 2
│   │       ├── Treatment Bay
│   │       └── Equipment Store
│   │
│   ├── Level 1
│   │   ├── ICU
│   │   │   ├── Bed Bay A
│   │   │   ├── Bed Bay B
│   │   │   └── Equipment Bay
│   │   └── Operating Theatre
│   │       ├── Theatre 1
│   │       ├── Theatre 2
│   │       ├── Theatre 3
│   │       └── Anaesthesia Store
│   │
│   ├── Level 2
│   │   ├── Cardiology
│   │   └── General Medicine
│   │
│   └── Level 3
│       ├── Pediatrics
│       └── Outpatient Services
│
├── Diagnostic & Imaging Centre
│   ├── Ground Floor
│   │   └── Radiology
│   │       ├── CT Room
│   │       ├── MRI Room
│   │       ├── X-Ray Room
│   │       ├── Ultrasound Room
│   │       └── Equipment Store
│   │
│   └── Level 1
│       └── Pathology & Laboratory
│           ├── Haematology
│           ├── Biochemistry
│           ├── Microbiology
│           └── Specimen Processing
│
└── Clinical Services Building
    └── Ground Floor
        ├── Pharmacy
        │   ├── Dispensary
        │   ├── Medication Store
        │   └── Cold Chain Store
        │
        └── Physiotherapy & Rehabilitation
            ├── Physiotherapy Gym
            ├── Hydrotherapy
            └── Equipment Store

## 8) Project Structure (Short)

```text
hospital-asset-management/
  backend/
  frontend/
  docs/
  reference_docs/
```

---
Agar chaho to main next step mein isi README ka "production deployment" section bhi add kar deta hoon (Docker / VPS / Vercel + Render style).
