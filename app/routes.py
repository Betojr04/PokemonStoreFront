from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from .models import db, Card, Transaction


main = Blueprint("main", __name__)

# File upload configurations
UPLOAD_FOLDER = "/path/to/your/uploads"  # Adjust this path as needed
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Route to add a new card
@main.route("/inventory/add", methods=["POST"])
def add_card():
    card_name = request.form["card_name"]
    edition = request.form["edition"]
    condition = request.form["condition"]
    quantity = int(request.form["quantity"])
    buy_price = request.form["buy_price"]

    image = request.files.get("card_image")
    image_path = None
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(UPLOAD_FOLDER, filename))
        image_path = os.path.join("uploads", filename)  # Adjust relative path as needed

    new_card = Card(
        card_name=card_name,
        edition=edition,
        condition=condition,
        quantity=quantity,
        buy_price=buy_price,
        image_path=image_path,
    )

    db.session.add(new_card)
    db.session.commit()

    flash("New card added successfully!", "success")
    return redirect(url_for("main.inventory"))


# Main landing page route
@main.route("/")
def index():
    return render_template("index.html", page_css="index.css")


# Inventory page route with dynamic cards list
@main.route("/inventory")
def inventory():
    cards = Card.query.all()
    return render_template("inventory.html", cards=cards, page_css="inventory.css")


# Transactions page route
@main.route("/transactions")
def transactions_page():
    return render_template("transactions.html", page_css="transactions.css")


# Selling card page route
@main.route("/sell-card")
def sell_card_page():
    return render_template("sell_card.html", page_css="sell_card.css")


# Edit card page route
@main.route("/edit-card")
def edit_card_page():
    return render_template("edit_card.html", page_css="edit_card.css")


# Route for editing a specific card
@main.route("/inventory/edit/<int:card_id>", methods=["GET", "POST"])
def edit_card(card_id):
    card = Card.query.get_or_404(card_id)
    if request.method == "POST":
        card.card_name = request.form["card_name"]
        card.edition = request.form["edition"]
        card.condition = request.form["condition"]
        card.quantity = int(request.form["quantity"])
        card.buy_price = request.form["buy_price"]

        # Update image if a new file is provided
        image = request.files.get("card_image")
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            card.image_path = os.path.join("uploads", filename)

        db.session.commit()
        flash("Card updated successfully!", "success")
        return redirect(url_for("main.inventory"))

    return render_template("edit_card.html", card=card, page_css="edit_card.css")


@main.route("/inventory/sell/<int:card_id>", methods=["GET", "POST"])
def sell_card(card_id):
    card = Card.query.get_or_404(card_id)

    if request.method == "POST":
        try:
            sell_quantity = int(request.form["sell_quantity"])
        except (ValueError, KeyError):
            flash("Invalid quantity provided.", "error")
            return redirect(url_for("main.sell_card", card_id=card.id))

        sell_price = request.form.get("sell_price")

        # Validate that we have enough inventory to complete the sale.
        if sell_quantity > card.quantity:
            flash("Not enough inventory to complete this sale.", "error")
            return redirect(url_for("main.sell_card", card_id=card.id))

        # Update the card inventory
        card.quantity -= sell_quantity

        # Create a new transaction record
        transaction = Transaction(
            card_id=card.id,
            quantity_sold=sell_quantity,
            sale_price=sell_price,  # Make sure your form properly sends a numeric value
        )
        db.session.add(transaction)
        db.session.commit()

        flash("Card sold successfully!", "success")
        return redirect(url_for("main.inventory"))

    return render_template("sell_card.html", card=card, page_css="sell_card.css")


@main.route("/transactions")
def transactions():
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).all()
    return render_template(
        "transactions.html", transactions=transactions, page_css="transactions.css"
    )


@main.route("/seller_dashboard")
def seller_dashboard():
    total_revenue = (
        db.session.query(
            db.func.sum(Transaction.quantity_sold * Transaction.sale_price)
        ).scalar()
        or 0
    )
    total_sold = db.session.query(db.func.sum(Transaction.quantity_sold)).scalar() or 0
    return render_template(
        "seller_dashboard.html",
        total_revenue=total_revenue,
        total_sold=total_sold,
        page_css="seller_dashboard.css",
    )
