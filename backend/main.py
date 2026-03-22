from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

import models
import schemas
import crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="OrderLink", description="WhatsApp-first food ordering")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../frontend/templates"))


# ─── Pages ────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@app.get("/menu/{seller_id}", response_class=HTMLResponse)
async def menu_page(request: Request, seller_id: str, db: Session = Depends(get_db)):
    seller = crud.get_seller(db, seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Menu not found")
    items = crud.get_menu_items(db, seller_id)
    return templates.TemplateResponse("menu.html", {
        "request": request,
        "seller": seller,
        "items": items,
    })


@app.get("/manage/{seller_id}", response_class=HTMLResponse)
async def manage_page(request: Request, seller_id: str, db: Session = Depends(get_db)):
    seller = crud.get_seller(db, seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    items = crud.get_menu_items(db, seller_id)
    return templates.TemplateResponse("manage.html", {
        "request": request,
        "seller": seller,
        "items": items,
    })


# ─── API Endpoints ─────────────────────────────────────────────────────────────

@app.post("/seller", response_model=schemas.SellerResponse)
async def create_seller(seller: schemas.SellerCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_seller(db, seller)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/menu-item", response_model=schemas.MenuItemResponse)
async def add_menu_item(item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    seller = crud.get_seller(db, item.seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    try:
        return crud.create_menu_item(db, item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/menu-item/{item_id}")
async def delete_menu_item(item_id: int, seller_id: str, db: Session = Depends(get_db)):
    deleted = crud.delete_menu_item(db, item_id, seller_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}


@app.get("/api/menu/{seller_id}", response_model=schemas.MenuResponse)
async def get_menu_api(seller_id: str, db: Session = Depends(get_db)):
    seller = crud.get_seller(db, seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Menu not found")
    items = crud.get_menu_items(db, seller_id)
    return {"seller": seller, "items": items}
