from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from . import models, schemas


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int):
    return db.query(models.Product).order_by(desc(models.Product.id)).limit(1).first()
    # return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_product_by_name(db: Session, product_name: str):
    return db.query(models.Product).filter(models.Product.name == product_name).first()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, description=product.description)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_upd: schemas.ProductCreate):
    # get the existing data
    db_product = db.query(models.Product).filter(models.Product.name == product_upd.name).one_or_none()
    if db_product is None:
        return create_product(db=db, product=product_upd)

    # Update model class variable from requested fields
    for var, value in vars(product_upd).items():
        setattr(db_product, var, value) if value else None

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if db_product is None:
        return False
    else:
        db.delete(db_product)
        db.commit()
        return True


def create_product_offer(db: Session, offer: schemas.OfferCreate, product_id: int):
    db_offer = models.Offer(**offer.dict(), product_id=product_id)
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer


def update_offers(db: Session):
    print("hello12")
    print("db_product.id = ")
    db_product = db.query(models.Product).order_by(desc(models.Product.id)).limit(1).first()
    print("db_product.id = ")
    # for i in range(1, db_product.id):
    #     print("hello22")
    #     pass
