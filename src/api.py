"""Module xử lý API calls đến Cellphones.vn"""

import requests

try:
    from .config import PRODUCTS, API_URL
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src.config import PRODUCTS, API_URL


def get_current_price(product_id, province_id):
    """Lấy giá hiện tại từ API Cellphones"""
    query = """
    query PRODUCT{
        product(
            id: "%s",
            provinceId: %s,
        ){
            filterable {
                price
                special_price
            }
        }
    }
    """ % (product_id, province_id)
    
    payload = {
        'query': query,
        'variables': {}
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers={
            'Content-Type': 'application/json'
        })
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and 'product' in data['data'] and data['data']['product']:
            product = data['data']['product']
            if 'filterable' in product:
                filterable = product['filterable']
                return {
                    'price': filterable.get('price'),
                    'special_price': filterable.get('special_price')
                }
        return None
    except Exception as e:
        print(f"Lỗi khi lấy giá: {e}")
        return None


if __name__ == '__main__':
    for p in PRODUCTS:
        print(f"\n{p['product_name']} (ID: {p['product_id']}):")
        result = get_current_price(p['product_id'], p['province_id'])
        if result:
            price = result.get('price')
            sp = result.get('special_price')
            print(f"  Giá gốc: {int(price):,} VNĐ" if price is not None else "  Giá gốc: N/A")
            print(f"  Giá khuyến mãi: {int(sp):,} VNĐ" if sp is not None else "  Giá khuyến mãi: N/A")
        else:
            print("  Không lấy được giá")
