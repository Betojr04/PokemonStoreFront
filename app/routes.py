from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html", page_css="index.css")


@main.route("/inventory")
def inventory():
    return render_template("inventory.html", page_css="inventory.css")


@main.route("/add-card")
def add_card():
    return render_template("add-card.html", page_css="add-card.css")


@main.route("/transactions")
def transactions():
    return render_template("transactions.html", page_css="transactions.css")
