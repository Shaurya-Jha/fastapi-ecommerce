import json
from pathlib import Path
from typing import Dict, List

DATA_FILE = Path("data", "products.json")


def load_products() -> List[Dict]:
    if not DATA_FILE.exists():
        print("data file does not exists")
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)


def get_all_products() -> List[Dict]:
    return load_products()


def save_product(products: List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)


def add_product(product: Dict) -> Dict:
    products = get_all_products()

    if any(p["sku"] == product["sku"] for p in products):
        raise ValueError("SKU already exists")

    products.append(product)
    save_product(products)
    return product


def remove_product(id: str):
    products = get_all_products()

    for idx, product in enumerate(products):
        if product["id"] == str(id):
            deleted = products.pop(idx)
            save_product(products)
            return {"message": "Product deleted successfully", "data": deleted}


def change_product(product_id: str, update_data: dict):
    products = get_all_products()

    for idx, product in enumerate(products):
        if product["id"] == product_id:
            for key, value in update_data.items():
                if value is None:
                    continue

                if isinstance(value, dict) and isinstance(product.get(key), dict):
                    product[key].update(value)
                else:
                    product[key] = value

            products[idx] = product
            save_product(products)
            return product

        raise ValueError("Product not found")
