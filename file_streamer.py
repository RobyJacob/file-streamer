from flask import Flask
from threading import Thread
from file_watcher import FileWatcher
from transactions import Transactions
from products import Products

import json


app = Flask(__name__)


@app.route("/assignment/transaction/<transaction_id>")
def get_transaction(transaction_id, methods=["GET"]):
    transaction = Transactions.get_transaction(transaction_id)
    product = Products.get_product(transaction.get("productId"))

    result = {
        "transactionId": transaction_id,
        "productName": product.get("productName"),
        "transactionAmount": transaction.get("transactionAmount"),
        "transactionDatetime": str(transaction.get("transactionDatetime"))
    }

    return f"{json.dumps(result)}"


@app.route("/assignment/transactionSummaryByProducts/<last_n_days>")
def get_transaction_summary_by_products(last_n_days, methods=["GET"]):
    summary_by_products = Transactions.get_summary_by_products(last_n_days)

    summary = {"summary": [
        {"productName": Products.get_product(product_id).get("productName"), "totalAmount": total_amount}
        for product_id, total_amount in summary_by_products.items()
    ]}

    return f"{json.dumps(summary)}"


@app.route("/assignment/transactionSummaryByManufacturingCity/<last_n_days>")
def get_transaction_summary_by_manufacturing_city(last_n_days, methods=["GET"]):
    summary_by_city = Transactions.get_summary_by_city(last_n_days)

    summary = {"summary": [
        {"cityName": city, "totalAmount": total_amount}
        for city, total_amount in summary_by_city.items()
    ]}

    return f"{json.dumps(summary)}"


if __name__ == "__main__":
    thread = Thread(target=FileWatcher.start, args=("data",))

    thread.daemon = True
    thread.start()

    app.run(port=8080)