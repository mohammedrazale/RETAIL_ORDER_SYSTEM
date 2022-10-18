""" Inventory Service. """
import sys
sys.path.append('/C:/UsersNahan/Desktop/RETAIL_ORDER_SYSTEM')
from flask import Flask, request
from RETAIL_ORDER_SYSTEM.inventory.db import engine
from RETAIL_ORDER_SYSTEM.inventory.model import InventoryProduct, create_db
from RETAIL_ORDER_SYSTEM.inventory.exceptions import NoSuchProductException
from RETAIL_ORDER_SYSTEM.helpers import send_success_response, send_bad_request_response

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Service Info."""
    return {"name": "ROS Inventory Service", "version": "0.0.1"}, 200


@app.route("/products", methods=["POST"])
def create_product():
    """Add a new product to the inventory."""
    required_fields = {"price", "stock", "name"}
    if required_fields != set(request.json.keys()):
        return send_bad_request_response("Required Fields are: price, stock, name")
    # Add new product to inventory & return the product
    product = InventoryProduct.create(
        request.json["name"], request.json["price"], request.json["stock"]
    )
    return send_success_response(product.as_dict())


@app.route("/products", methods=["GET"])
@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id=None):
    """Get all products or return a specific product."""
    if not product_id:
        results = []
        for product in InventoryProduct.get_all():
            results.append(product.as_dict())
        return send_success_response(results)
    try:
        return send_success_response(InventoryProduct(product_id).as_dict())
    except NoSuchProductException:
        return send_bad_request_response(f"No product with the id {product_id}")


@app.route("/products/<int:product_id>", methods=["PATCH"])
def update_products(product_id=None):
    """Update details of product in inventory."""
    _valid_fields = {"price", "stock", "name"}
    for key in request.json.keys():
        if key not in _valid_fields:
            return send_bad_request_response("Updatable Fields are: price, stock, name")

    updated_product = InventoryProduct(product_id).update(request.json)
    return send_success_response(updated_product.as_dict())


if __name__ == "__main__":
    # create db if not already present
    create_db(engine)
    app.run(host="0.0.0.0", port=5500)
