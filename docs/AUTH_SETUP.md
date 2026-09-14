# AssetCare authentication setup

## 1. Create the Supabase project

1. Open [supabase.com](https://supabase.com), create an account, and create a new project.
2. Choose a strong database password and keep it somewhere secure.
3. Open **Project Settings > Database > Connection string > URI**.
4. Copy the URI, replace `[YOUR-PASSWORD]` with the database password, and change its prefix from `postgresql://` to `postgresql+psycopg://`.
5. In `Backend`, copy `.env.example` to `.env` and set `DATABASE_URL` to that URI.
6. Replace `JWT_SECRET` with a long random value. Never commit `.env`.

The FastAPI service creates its `users` table on first start. Passwords are stored as Argon2 hashes; the raw password is never stored.

## 2. Configure and run the backend

```powershell
cd Backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Verify `http://localhost:8000/api/health` returns `{"status":"healthy"}`.

## 3. Configure and run the frontend

In `frontend`, copy `.env.example` to `.env` (the default URL is already correct), then run:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000/auth/register`. A new account can be registered as Nurse, Biomedical Engineer, or Manager. The API returns a JWT and the frontend lands on the matching dashboard immediately. Login uses the saved role from the database, never the email text.

## 4. Create an administrator

Admin self-registration is intentionally blocked. After registering a trusted account, promote it in Supabase **SQL Editor**:

```sql
update public.users
set role = 'admin'
where email = 'admin@example.com';
```

Then log in again; the user will land on `/admin/dashboard`.

## Notes

- Use the Supabase **direct** connection string for local development if the pooler is unavailable. Keep `sslmode=require`.
- For production, set `FRONTEND_URL` to the exact deployed frontend origin and use a strong secret stored in the host's environment settings.
- This project uses its own FastAPI JWT auth and Supabase Postgres as the database. Supabase Auth is not required for this flow, so do not expose the Supabase service-role key to Nuxt.
