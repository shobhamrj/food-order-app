from typing import Tuple
from fastapi import FastAPI, HTTPException, Depends
from passlib.hash import bcrypt
from fastapi.middleware.cors import CORSMiddleware
from models import *
from auth import get_current_user, authenticate_user, create_token
from db import cursor, mysql_conn

# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles


app = FastAPI()

# templates = Jinja2Templates(directory="templates")
# app.mount('/static', StaticFiles(directory='./templates'), name='js')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/signup", response_class=HTMLResponse)
# async def signup(request: Request):
#     return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/v1/signup")
async def signup(user: User):
    hashed_password = bcrypt.hash(user.password)
    cursor.execute(
        "INSERT INTO users (email, name, password) VALUES (%s, %s, %s)",
        (user.email, user.name, hashed_password),
    )
    mysql_conn.commit()
    return {"message": "User created successfully"}


@app.post("/v1/login")
async def login(user: User):
    user = authenticate_user(user.email, user.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_token(user[0])
    return {"access_token": token}


@app.post("/v1/order")
async def create_order(order: Order, user: User = Depends(get_current_user)):
    cursor.execute(
        "INSERT INTO orders (user_id, total_price) VALUES (%s, %s)",
        (user[0], order.total_price),
    )
    order_id = cursor.lastrowid
    for food_item in order.food_items:
        cursor.execute(
            "INSERT INTO order_items (order_id, name, quantity, unit_price) VALUES (%s, %s, %s, %s)",
            (order_id, food_item.name, food_item.quantity, food_item.unit_price),
        )
    mysql_conn.commit()
    return {"message": "Order created successfully"}


@app.get("/v1/orders")
async def get_orders(user: User = Depends(get_current_user)):
    cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user[0],))
    orders = cursor.fetchall()
    response = []
    for order in orders:
        cursor.execute("SELECT * FROM order_items WHERE order_id = %s", (order[0],))
        items = cursor.fetchall()
        food_items = [
            {
                "name": item[2],
                "quantity": item[3],
                "unit_price": item[4]
            }
            for item in items
        ]
        response.append({
            "order_id": order[0],
            "food_items": food_items,
            "total_price": order[2]
        })
    return response


@app.get("/v1/order/{order_id}")
async def get_order(order_id: int, user: User = Depends(get_current_user)):
    cursor.execute("SELECT * FROM orders WHERE id = %s AND user_id = %s", (order_id, user[0]))
    order = cursor.fetchone()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    cursor.execute("SELECT * FROM order_items WHERE order_id = %s", (order[0],))
    items = cursor.fetchall()
    food_items = [
        {
            "name": item[2],
            "quantity": item[3],
            "unit_price": item[4]
        }
        for item in items
    ]
    return {
        "order_id": order[0],
        "food_items": food_items,
        "total_price": order[2]
    }


@app.put("/v1/order/{order_id}")
async def update_order(order_id: int, order: Order, user: Tuple[int] = Depends(get_current_user)):
    cursor.execute("SELECT * FROM orders WHERE id = %s AND user_id = %s", (order_id, user[0]))
    existing_order = cursor.fetchone()
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")
    cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
    for food_item in order.food_items:
        cursor.execute(
            "INSERT INTO order_items (order_id, name, quantity, unit_price) VALUES (%s, %s, %s, %s)",
            (order_id, food_item.name, food_item.quantity, food_item.unit_price),
        )
    cursor.execute(
        "UPDATE orders SET total_price = %s WHERE id = %s",
        (order.total_price, order_id),
    )
    mysql_conn.commit()
    return {"message": "Order updated successfully"}


@app.delete("/v1/order/{order_id}")
async def delete_order(order_id: int, user: User = Depends(get_current_user)):
    cursor.execute("SELECT * FROM orders WHERE id = %s AND user_id = %s", (order_id, user[0]))
    existing_order = cursor.fetchone()
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")
    cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
    cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
    mysql_conn.commit()
    return {"message": "Order deleted successfully"}
