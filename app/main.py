from datetime import datetime
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from services.products import add_product, change_product, get_all_products, remove_product
from schema.product import Product, ProductUpdate

app = FastAPI()

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

    return JSONResponse({"total": total_products, "limit": limit, "products": products}, status_code=status.HTTP_200_OK)

@app.get('/products/{product_id}')
def get_product_by_id(product_id: str):
    products = get_all_products()
    
    for product in products:
        if product.get("id") == product_id:
            return JSONResponse(product)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

@app.post('/products', status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    product_dict = product.model_dump(mode='json')
    product_dict['id'] = str(uuid4())
    product_dict['created_at'] = datetime.now().isoformat() + 'Z'

    try:
        add_product(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return product.model_dump(mode='json')

@app.delete('/products/{product_id}')
def delete_product(product_id: UUID):
    try:
        res = remove_product(str(product_id))
        return res
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.put("/products/{product_id}")
def update_product(product_id: UUID, payload: ProductUpdate):
    try:
        update_product = change_product(str(product_id), payload.model_dump(mode='json', exclude_unset=True))

        return update_product
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))