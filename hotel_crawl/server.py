from flask import Flask, jsonify, request
from models import db_connect, Hotel, Tour
from sqlalchemy.orm import sessionmaker, scoped_session
from scrapy.utils.project import get_project_settings
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS


engine = db_connect()
db_session = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = get_project_settings().get(
    "CONNECTION_STRING")
# db = SQLAlchemy(app)
ma = Marshmallow(app)
app.config['DEFAULT_PARSERS'] = [
    'flask.ext.api.parsers.JSONParser',
    'flask.ext.api.parsers.URLEncodedParser',
    'flask.ext.api.parsers.MultiPartParser'
]
CORS(app)


class HotelSchema(ma.SQLAlchemyAutoSchema):  # noqa
    class Meta:
        model = Hotel


class TourSchema(ma.SQLAlchemyAutoSchema):  # noqa
    class Meta:
        model = Tour


hotel_schema = HotelSchema(many=True)
tour_schema = TourSchema(many=True)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/api/recommendation", methods=["GET", "POST"])
def recommendation():
    json_data = request.get_json(silent=True)
    city_id = json_data["city_id"]
    hotels = Hotel.query.filter_by(city_id=city_id).limit(10).all()
    tours = Tour.query.filter_by(city_id=city_id).all()

    hotels = hotel_schema.dump(hotels)
    tours = tour_schema.dump(tours)
    return jsonify({"hotels": hotels, "tours": tours})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
