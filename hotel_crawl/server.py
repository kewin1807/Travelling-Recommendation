from flask import Flask, jsonify
from models import db_connect, Hotel, Tour
from sqlalchemy.orm import sessionmaker, scoped_session
from scrapy.utils.project import get_project_settings
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

engine = db_connect()
db_session = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = get_project_settings().get(
    "CONNECTION_STRING")
# db = SQLAlchemy(app)
ma = Marshmallow(app)


class HotelSchema(ma.SQLAlchemyAutoSchema):  # noqa
    class Meta:
        model = Hotel


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/api/recommendation", methods=["GET"])
def recommendation():

    hotels = Hotel.query.limit(5).all()
    for hotel in hotels:
        print(hotel.hotel_name)
    hotel_schema = HotelSchema(many=True)
    hotels = hotel_schema.dump(hotels)
    return jsonify({"hotels": hotels})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
