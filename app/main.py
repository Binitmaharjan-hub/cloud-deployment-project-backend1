from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .database import SessionLocal

app = FastAPI(title="Catalog-Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"service": "catalog", "status": "ok"}


@app.get("/products")
def get_products():

    with SessionLocal() as db:

        rows = db.execute(text("""
            SELECT
                id,
                name,
                price
            FROM products
            ORDER BY id
        """))

        return [
            {
                "id": r.id,
                "name": r.name,
                "price": float(r.price)
            }
            for r in rows
        ]


@app.get("/products/{product_id}")
def get_product(product_id: int):

    with SessionLocal() as db:

        row = db.execute(
            text("""
                SELECT
                    id,
                    name,
                    price
                FROM products
                WHERE id=:id
            """),
            {"id": product_id}
        ).fetchone()

        return {
            "id": row.id,
            "name": row.name,
            "price": float(row.price)
        }