from topsis import topsis
from geopy.distance import geodesic
TOPSIS_WEIGHT_HOTEL = [0.2, 0.3, 0.1, 0.1, 0.3]
TOPSIS_WEIGHT_TOUR = [0.3, 0.1, 0.25, 0.2, 0.15]

# Information on benefit (1) cost (0) criteria should be provided in I.
TOPSIS_I_HOTEL = [1, 1, 0, 0, 1]
TOPSIS_I_TOUR = [1, 0, 1, 1, 0]

TOPSIS_INFORMATION_HOTEL = []
HOTEL_FEATURES = ["quality", "rating", "number_people_rating",
                  "distance_calc", "price"]
TOUR_FEATURES = ["rating_tour", "number_people_rating",
                 "price", "number_available_seat", "number_days"]


def calc_distance(hotel_coordination, user_coordination):
    hotel_coordinations = hotel_coordination.split(",")
    hotel_location = (
        float(hotel_coordinations[1]), float(hotel_coordinations[0]))
    return round(geodesic(hotel_location, user_coordination).miles, 2)


def ranking_topsis(df, type_topsis="hotel"):
    weights = []
    I = []
    features = []
    if type_topsis == "hotel":
        weights = TOPSIS_WEIGHT_HOTEL
        I = TOPSIS_I_HOTEL
        features = HOTEL_FEATURES
    else:
        weights = TOPSIS_WEIGHT_TOUR
        I = TOPSIS_I_TOUR
        features = TOUR_FEATURES
    a = df[features].values.tolist()
    print(df[features])
    print(a)
    decision = topsis(a, weights, I)
    decision.calc()
    probilities = decision.C
    indexes = decision.optimum_choice
    return probilities, indexes
