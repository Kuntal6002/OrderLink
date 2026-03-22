# OrderLink – Deployment Guide

## Local Development

```bash
# 1. Clone / enter the project
cd orderlink

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
cd backend
uvicorn main:app --reload --port 8000
```

Open: http://localhost:8000

---

## Deploy to Railway (Recommended – Free)

1. Go to https://railway.app and sign up
2. Click **New Project → Deploy from GitHub**
3. Connect your GitHub repo
4. Set the **Start Command** to:
   ```
   uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```
5. Railway auto-detects `requirements.txt` and installs deps
6. Click **Deploy** → get your public URL!

### Environment Variables (Railway)
| Variable | Value |
|---|---|
| `DATABASE_URL` | Leave blank (uses SQLite by default) |

> For production with many sellers, upgrade to PostgreSQL:
> Set `DATABASE_URL=postgresql://user:pass@host/db`

---

## Deploy to Render (Alternative – Free Tier)

1. Go to https://render.com and sign up
2. Click **New → Web Service**
3. Connect your GitHub repo
4. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: Leave blank
5. Click **Create Web Service**

---

## Project Structure

```
orderlink/
├── backend/
│   ├── main.py          # FastAPI app, routes, pages
│   ├── models.py        # SQLAlchemy ORM models
│   ├── database.py      # DB connection, session
│   ├── schemas.py       # Pydantic validation schemas
│   └── crud.py          # Database operations
├── frontend/
│   └── templates/
│       ├── create.html  # Seller onboarding page
│       ├── menu.html    # Public customer menu page
│       └── manage.html  # Seller item management
├── requirements.txt
├── Procfile
└── DEPLOY.md
```

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Seller creation page |
| POST | `/seller` | Create a seller, get seller_id |
| POST | `/menu-item` | Add item to a menu |
| DELETE | `/menu-item/{id}?seller_id=...` | Remove an item |
| GET | `/menu/{seller_id}` | Public menu page |
| GET | `/manage/{seller_id}` | Seller management page |
| GET | `/api/menu/{seller_id}` | Menu JSON API |

---

## Example Usage

1. Seller goes to your app URL
2. Enters name ("Riya's Kitchen") + WhatsApp number (9876543210)
3. Gets link: `https://yourapp.com/menu/abc-123-def`
4. Goes to `/manage/abc-123-def`, adds:
   - Maggi → ₹30
   - Chai → ₹15
   - Cold Coffee → ₹50
5. Shares the menu link on WhatsApp groups
6. Customer opens link, selects items, taps "Order on WhatsApp"
7. WhatsApp opens with pre-filled message:

```
Hi 👋
I want to order from *Riya's Kitchen*:

• 2 × Maggi - ₹60
• 1 × Cold Coffee - ₹50

*Total: ₹110*

Name: Rahul Kumar
Address: Room 204, Hostel A
```

Riya receives this on WhatsApp and confirms the order!
