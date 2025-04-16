from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(100), nullable=False)
    edition = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(40), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    buy_price = db.Column(db.Numeric(10, 2), nullable=False)
    image_path = db.Column(db.String(200))


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"), nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False)
    sale_price = db.Column(db.Numeric(10, 2), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Creating a relationship so you can easily access the card details from a transaction:
    card = db.relationship("Card", backref=db.backref("transactions", lazy=True))
