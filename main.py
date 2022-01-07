from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
from markupsafe import escape

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

    def to_dict(self):
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route("/random")
def get_random_coffee():
    cafes = db.session.query(Cafe).all()
    random_coffee = random.choice(cafes)
    return jsonify(cafe=random_coffee.to_dict())


## return all the cafes in database as a JSON
@app.route("/all")
def get_all_cafes():
    cafes = db.session.query(Cafe).all()
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])


## to search for cafes at a particular location.
@app.route("/search")
def search_cafe():
    query_location = request.args.get("loc")
    cafe_location = db.session.query(Cafe).filter_by(location=query_location).first()
    if cafe_location is not None:
        return jsonify(cafe=cafe_location.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location"})


# Convert String to Boolean
def str_to_boolean(value):
    if value in ['YES', 'Y', 'yes', 'y', '1', 'True', 'true', 'T', 't']:
        return True
    else:
        return False


## HTTP POST - Create Record
@app.route("/add", methods=["GET", "POST"])
def post_new_cafe():
    # Create row from value request.form
    new_cafe = Cafe(
        name=request.form['name'],
        map_url=request.form['map_url'],
        img_url=request.form['img_url'],
        location=request.form['location'],
        seats=request.form['seats'],
        has_toilet=str_to_boolean(request.form['has_toilet']),
        has_wifi=str_to_boolean(request.form['has_wifi']),
        has_sockets=str_to_boolean(request.form['has_sockets']),
        can_take_calls=str_to_boolean(request.form['can_take_calls']),
        coffee_price=request.form['coffee_price']
    )

    # add row to database
    db.session.add(new_cafe)
    db.session.commit()

    # Return Success
    return jsonify(response={"Success": "Successfully added the new cafe"})


## HTTP PUT/PATCH - Update Record

# Update the coffee_price field of the cafe.
@app.route("/update-price/<cafe_id>", methods=['PATCH'])
def update_price(cafe_id):
    cafe = Cafe.query.get(escape(cafe_id))
    if cafe:
        cafe_price = request.args.get('new_price')
        cafe.price = cafe_price
        db.session.commit()
        return jsonify(success="Successfully updated the price to {}".format(cafe_price))
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})


## HTTP DELETE - Delete Record

# Delete a cafe that's closed
@app.route("/report-closed/<cafe_id>", methods=['DELETE'])
def delete_cafe(cafe_id):
    api_key = request.args.get('api-key')
    cafe_id = escape(cafe_id)
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        if api_key == "TopSecretAPIKey":
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(success="Successfully deleted with id: {}".format(cafe_id)), 200
        else:
            return jsonify(error="Sorry, that's not allowed. Make sure you have the correct api_key."), 404
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 403


if __name__ == '__main__':
    app.run(debug=True)
