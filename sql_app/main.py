from typing import List

import uvicorn
from time import time
import aiohttp
import asyncio
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
token_URL = "https://applifting-python-excercise-ms.herokuapp.com/api/v1"

scheduler = BackgroundScheduler()


def get_token():
    pass


async def request(session):
    async with session.post(token_URL + '/auth') as response:
        return await response.text()


async def task():
    async with aiohttp.ClientSession() as session:
        tasks = request(session)
        result = await asyncio.gather(tasks)
        print(result)


# @app.on_event("startup")
# async def startup_event():
    # await task()
    # print("Hello world")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/product/{user_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_name(db, product_name=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product name already registered")
    return crud.create_product(db=db, product=product)


@app.put("/products/", response_model=schemas.Product)
def update_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.update_product(db=db, product_upd=product)


@app.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    if not crud.delete_product(db=db, product_id=product_id):
        raise HTTPException(status_code=404, detail="Product not found")

