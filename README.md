RETAIL ORDERING SYSTEM- BACKEND
Note:
-----
    Add Folder above RETAIL_ORDER_SYSTEM to PYTHONPATH

Dependencies
------------
    Python >= 3.6

Quickstart
----------
    $ python -m venv venv
    $ .\venv\Scripts\activate
    $ pip install -r .\requiremets.txt
    (tab 1)$ python RETAIL_ORDER_SYSTEM\inventory\service.py
    (tab 2)$ python RETAIL_ORDER_SYSTEM\order\service.py


Inventory Service
(please refer postman_collection)
=================

    GET http://localhost:5500/products
    GET http://localhost:5500/products/1
    PATCH http://localhost:5500/products/1
        body (raw):
            {
                "stock": 50,
                "price": 5.5,
                "name": "Pencil"
            }
        header:
            Content-Type: application/json
    POST http://localhost:5500/products
        body (raw):
            {
                "stock": 50,
                "price": 5.5,
                "name": "Pencil Dark"
            }
        header:
            Content-Type: application/json

Order Service
(please refer postman_collection):
=============

    GET http://localhost:5000/orders
    GET http://localhost:5000/orders/1
    PATCH http://localhost:5000/orders/1
        body(raw):
            {
                "status": "complete"
            }
        header:
            Content-Type: application/json
    POST http://localhost:5000/orders
        body(raw):
            {
                "user_name": "r2",
                "user_ph_no": "1234",
                "user_address": "abc, xyz",
                "product_id": 1,
                "qty": 3
            }
        header:
            Content-Type: application/json
    DEL http://localhost:5000/orders/1
