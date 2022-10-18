""" Order Service. """

import json
import requests
from flask import Flask, request
from RETAIL_ORDER_SYSTEM.helpers import (
    send_success_response,
    send_bad_request_response,
    send_server_error_response,
)
from RETAIL_ORDER_SYSTEM.order.db import engine
from RETAIL_ORDER_SYSTEM.order.model import Order, create_db
from RETAIL_ORDER_SYSTEM.order.exceptions import NoSuchOrderException

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Service Info."""
    return {"name": "RETAL ORDER SYSTEM Order Service", "version": "0.0.1"}, 200


@app.route("/orders", methods=["POST"])
def create_order():
    """Create a new Order."""
    required_fields = {"user_name", "user_ph_no", "user_address", "product_id", "qty"}
    if required_fields != set(request.json.keys()):
        return send_bad_request_response(
            "Required Fields are: user_name, user_ph_no, user_address, product_id, qty"
        )

    product_id = request.json["product_id"]
    try:
        resp = requests.get(f"http://localhost:5500/products/{product_id}")
    except requests.exceptions.RequestException:
        return send_server_error_response("Unable to fetch product info")

    if resp.status_code == 400:
        return send_bad_request_response(f"No product with the id {product_id}")

    if resp.status_code == 200:
        product_info = resp.json()["result"]
        if product_info["stock"] < request.json["qty"]:
            return send_bad_request_response(
                f"Stock ({product_info['stock']}) < requested ({request.json['qty']})"
            )
        try:
            headers = {"Content-Type": "application/json"}
            req = requests.patch(
                f"http://localhost:5500/products/{product_id}",
                headers=headers,
                data=json.dumps({"stock": product_info["stock"] - request.json["qty"]}),
            )
            if req.status_code == 200:
                order = Order.create(request.json)
                return send_success_response(order.as_dict())
            return send_server_error_response("Unable to update product info")
        except requests.exceptions.RequestException:
            return send_server_error_response("Unable to update product info")

    return send_server_error_response("Unable to fetch product info")


@app.route("/orders", methods=["GET"])
@app.route("/orders/<int:order_id>", methods=["GET"])
def get_orders(order_id=None):
    """Get all products from products table."""

    if not order_id:
        results = []
        for order in Order.get_all():
            results.append(order.as_dict())
        return send_success_response(results)

    try:
        order = Order(order_id)
        return send_success_response(order.as_dict())
    except NoSuchOrderException:
        return send_bad_request_response(f"No Order with the id {order_id}")


@app.route("/orders/<int:order_id>", methods=["PATCH"])
def update_order(order_id=None):
    """Update Order."""
    _valid_fields = {
        "user_name",
        "user_ph_no",
        "user_address",
        "qty",
        "status",
    }
    for key in request.json.keys():
        if key not in _valid_fields:
            return send_bad_request_response(
                "Updatable Fields are: user_name, user_address, user_address, qty, status"
            )

    order = Order(order_id)
    order.update(request.json)
    return send_success_response(order.as_dict())


@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id=None):
    """Delete an order."""
    try:
        order = Order(order_id)
    except NoSuchOrderException:
        return send_bad_request_response(f"No order with the id {order_id}")

    if order.status == "complete":
        return send_bad_request_response("Cannot delete a completed order.")

    try:
        resp = requests.get(f"http://localhost:5500/products/{order.product_id}")
    except requests.exceptions.RequestException:
        return send_server_error_response("Unable to fetch product info")

    if resp.status_code == 400:
        return send_bad_request_response(f"No product with the id {order.product_id}")

    if resp.status_code == 200:
        product_info = resp.json()["result"]
        try:
            headers = {"Content-Type": "application/json"}
            req = requests.patch(
                f"http://localhost:5500/products/{order.product_id}",
                headers=headers,
                data=json.dumps({"stock": product_info["stock"] + order.qty}),
            )
            if req.status_code == 200:
                order.delete()
                return send_success_response(order.as_dict())
            return send_server_error_response("Unable to update product info")
        except requests.exceptions.RequestException:
            return send_server_error_response("Unable to update product info")

    return send_server_error_response("Unable to fetch product info")


if __name__ == "__main__":
    # create db if not already present
    create_db(engine)
    app.run(host="0.0.0.0", port=5000)
