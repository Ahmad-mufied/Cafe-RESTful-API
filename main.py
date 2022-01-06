from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route("/random")
def get_random_coffee():
    coffes = db.session.query(Cafe).all()
    random_coffee = random.choice(coffes)
    return jsonify(
        cafe={
            "can_take_calls": random_coffee.can_take_calls,
            "coffee_price": random_coffee.coffee_price,
            "has_sockets": random_coffee.has_sockets,
            "has_toilet": random_coffee.has_toilet,
            "has_wifi": random_coffee.has_wifi,
            "id": random_coffee.id,
            "img_url": random_coffee.img_url,
            "location": random_coffee.location,
            "map_url": random_coffee.map_url,
            "name": random_coffee.name,
            "seats": random_coffee.seats
        }
    )

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
