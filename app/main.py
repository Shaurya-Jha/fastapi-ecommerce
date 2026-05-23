from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from services.product import get_all_products

app = FastAPI()


@app.get("/")
def root():
    return JSONResponse({"message": "Server connection successfull"})


@app.get("/products")
def list_products(
    name: str = Query(
        default=None, min_length=1, max_length=50, description="Search product by name"
    ),
    sort_by_price: bool = Query(default=False, description="Sort products by price"),
    order: str = Query(
        default="asc", description="Sort order when sort_by_price=true (asc, desc)"
    ),
    limit: int = Query(
        default=10, ge=1, le=100, description='Number of items to return'
    ),
    offset: int = Query(
        default=0, ge=0, description="Pagination offset"
    )
):
    products = get_all_products()
    total_products = len(products)
    
    if name:
        sanitized_name = name.strip().lower()
        products = [prod for prod in products if sanitized_name in prod.get("name", "").lower()]

    if sort_by_price:
        reverse = order == "desc"
        products = sorted(products, key=lambda p: p.get("price", 0), reverse=reverse)

    if limit:
        products = products[offset : offset + limit]

    if not products:
        raise HTTPException(status_code=404, detail="No product found")

    return JSONResponse({"total": total_products, "limit": limit, "products": products})
