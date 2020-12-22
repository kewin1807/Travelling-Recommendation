from flask import Flask, jsonify, request
from models import db_connect, Hotel, Tour
from sqlalchemy.orm import sessionmaker, scoped_session
from scrapy.utils.project import get_project_settings
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import pandas as pd
from constant import LIST_CENTER_CITY
from utils import calc_distance, ranking_topsis
df_hotels = pd.read_csv("hotel.csv")
df_tours = pd.read_csv("tour.csv")

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


def filter_by_price_hotel(df, type_price):
    if len(df) == 0:
        return df
    # type = 0 < 400.000 vnd
    # type = 1 400.000 => 1.000.000
    # type = 2 1.000.000 => 2.000.000
    # type = 3 > 2.000.000
    LIST_PRICE = {
        "0": [0, 400000],
        "1": [400000, 1000000],
        "2": [1000000, 2000000],
        "3": [2000000, 9999999999]
    }
    return df[(df['price'] >= LIST_PRICE[type_price][0]) & (df['price'] <= LIST_PRICE[type_price][1])]


def filter_by_price_tour(df, type_price):
    if len(df) == 0:
        return df

    # type = 0 < 2.000.000 vnd
    # type = 1 2.000.000 => 4.000.000
    # type = 2 4.000.000 => 8.000.000
    # type = 3 > 8.000.000

    LIST_PRICE = {
        "0": [0, 2000000],
        "1": [2000000, 4000000],
        "2": [4000000, 8000000],
        "3": [8000000, 1000000000]
    }
    return df[(df['price'] >= LIST_PRICE[type_price][0]) & (df['price'] <= LIST_PRICE[type_price][1])]


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/api/recommendation", methods=["GET", "POST"])
def recommendation():
    json_data = request.get_json(silent=True)
    df_hotels_return = df_hotels
    df_tour_return = df_tours
    if "city_id" in json_data:
        df_hotels_return = df_hotels_return[df_hotels_return["city_id"]
                                            == int(json_data["city_id"])]

        df_tour_return = df_tour_return[df_tour_return["city_id"]
                                        == int(json_data["city_id"])]
    if "type_price_hotel" in json_data and json_data["type_price_hotel"] != "-1":
        df_hotels_return = filter_by_price_hotel(
            df_hotels_return, type_price=json_data["type_price_hotel"])
    if "type_price_tour" in json_data and json_data["type_price_tour"] != "-1":
        df_tour_return = filter_by_price_tour(
            df_tour_return, type_price=json_data["type_price_tour"])
    center_location = LIST_CENTER_CITY[json_data["city_id"]]

    if len(df_hotels_return) > 0:
        df_hotels_return["distance_calc"] = df_hotels_return["distance"].apply(
            lambda x: calc_distance(x, center_location))

        prob_hotels, hotel_idxes = ranking_topsis(
            df_hotels_return, type_topsis="hotel")
        df_hotels_return = df_hotels_return.iloc[hotel_idxes]

    if len(df_tour_return) > 0:

        prob_tours, tour_idxes = ranking_topsis(
            df_tour_return, type_topsis="tour")

        df_tour_return = df_tour_return.iloc[tour_idxes]
    return jsonify({"hotels": eval(df_hotels_return.to_json(orient="records")), "tours": eval(df_tour_return.to_json(orient="records"))})

    # city_id = json_data["city_id"]
    # hotels = Hotel.query.filter_by(city_id=city_id).limit(10).all()
    # tours = Tour.query.filter_by(city_id=city_id).all()
    # hotels = hotel_schema.dump(hotels)
    # tours = tour_schema.dump(tours)
    # return jsonify({"hotels": hotels, "tours": tours})
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
