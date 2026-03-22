from sqlalchemy.orm import Session
import models
import schemas
import uuid


def create_seller(db: Session, seller: schemas.SellerCreate) -> models.Seller:
    db_seller = models.Seller(
        id=str(uuid.uuid4()),
        name=seller.name.strip(),
        phone=seller.phone.strip()
    )
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller


def get_seller(db: Session, seller_id: str) -> models.Seller | None:
    return db.query(models.Seller).filter(models.Seller.id == seller_id).first()


def create_menu_item(db: Session, item: schemas.MenuItemCreate) -> models.MenuItem:
    db_item = models.MenuItem(
        seller_id=item.seller_id,
        name=item.name.strip(),
        price=item.price,
        image_url=item.image_url.strip() if item.image_url else None
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_menu_items(db: Session, seller_id: str) -> list[models.MenuItem]:
    return db.query(models.MenuItem).filter(models.MenuItem.seller_id == seller_id).all()


def delete_menu_item(db: Session, item_id: int, seller_id: str) -> bool:
    item = db.query(models.MenuItem).filter(
        models.MenuItem.id == item_id,
        models.MenuItem.seller_id == seller_id
    ).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True
