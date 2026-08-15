from fastapi import FastAPI , HTTPException
from pydantic import BaseModel 
import json
import os

app = FastAPI()

class Restraunt(BaseModel):
    table_id : int
    order : dict

#load_menu
def load_data():
    with open('menu.json','r') as f:
        data = json.load(f)
    return data

#save the order
def save_data(data):
    with open('orders.json','w') as f:
        json.dump(data,f)

#load orders 
def load_orders():
    if not os.path.exists('orders.json'):
        return {}
    with open('orders.json','r') as f:
        content = f.read().strip()
        if not content:
            return {}
        return json.loads(content)

# helper: find an item's price by searching all categories
def find_item(menu, item_name):
    for category, items in menu.items():
        if item_name in items:
            return items[item_name], category
    return None, None

# order 
@app.post('/{table_id}/order')
def order(table_id: int, restraunt: Restraunt):
    # load menu
    data = load_data()

    # select order
    selected_items = []
    total = 0 
    for item_name, qty in restraunt.order.items():
        price, category = find_item(data, item_name)
        if price is None:
            raise HTTPException(status_code = 404,detail=f"Item {item_name} not found in menu")
        subtotal = price*qty
        total += subtotal
        selected_items.append({
            "Name":item_name,
            "Price":price,
            "Category":category,
            "Quantity":qty,
            "Total":subtotal,
        })


    # save the order 
    all_orders = load_orders()
    all_orders[str(table_id)] = {
        "items": selected_items,
        "total": total,
        "status": "placed"
    }
    save_data(all_orders)

#order add 
@app.put('/{table_id}/edit/order')
def add_order(table_id:int):
    pass

#chef getting orders
@app.get('/get/{table_id}')
def get_orders(table_id:int):
    pass