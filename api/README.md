# KBD School API — Backend README

FastAPI backend for K.B.D. English Medium School website.

- **Local DB**: SQLite (zero setup, automatic)
- **Production DB**: Neon PostgreSQL (free tier)

---

## Local Development

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the API server
```bash
# From the project root
uvicorn api.index:app --reload --port 8000
```

### 3. Open the interactive API docs
```
http://localhost:8000/api/docs
```

---

## API Endpoints

| Method   | Endpoint                    | Description                        |
|----------|-----------------------------|------------------------------------|
| GET      | `/api/health`               | Health check                       |
| POST     | `/api/admissions`           | Submit admission enquiry           |
| GET      | `/api/admissions`           | List all enquiries (admin)         |
| DELETE   | `/api/admissions/{id}`      | Delete an enquiry                  |
| GET      | `/api/events`               | List all events/gallery items      |
| POST     | `/api/events`               | Add a new event                    |
| PUT      | `/api/events/{id}`          | Update an event                    |
| DELETE   | `/api/events/{id}`          | Delete an event                    |

---

## Production Setup with Neon (Free PostgreSQL)

1. Go to **[neon.tech](https://neon.tech)** → Sign up free (no credit card needed)
2. Click **"New Project"** → Choose a region close to India (Singapore or US East)
3. Copy the **Connection String** (looks like `postgresql://user:pass@ep-xxx.neon.tech/neondb`)
4. In **Vercel Dashboard** → Your Project → **Settings → Environment Variables**
5. Add: `DATABASE_URL` = `your_neon_connection_string?sslmode=require`
6. Redeploy → tables are created automatically on first request

### Free Tier Limits (Neon)
- Storage: **0.5 GB** (enough for thousands of form submissions)
- Compute: **100 hours/month** (scales to zero when not in use)
- No credit card required

---

## Deploying to Vercel

The `api/index.py` is automatically detected as a Python serverless function.

```bash
git add .
git commit -m "Add FastAPI backend"
git push origin main
# Vercel auto-deploys on push
```

Set `DATABASE_URL` in Vercel environment variables (see above).
