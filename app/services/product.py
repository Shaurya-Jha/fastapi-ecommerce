import json
from pathlib import Path
from typing import List, Dict

DATA_FILE = Path( 'data', 'products.json')

def load_products() -> List[Dict]:
    if not DATA_FILE.exists():
        print('data file does not exists')
        return []
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def get_all_products() -> List[Dict]:
    return load_products()