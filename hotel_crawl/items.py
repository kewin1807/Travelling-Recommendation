# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
import re
# Importing the required libraries
import contextlib
from urllib.parse import urlencode
import sys
from urllib.request import urlopen
import gdshortener
# Defining the function to shorten a URL

s = gdshortener.ISGDShortener()


def make_shorten(url):
    return s.shorten(url)


DOMAIN_HOTEL = "https://www.booking.com"
DOMAIN_TOUR = "https://travel.com.vn"


def parseDistance(text):
    return text


def parseFloatNumber(text):
    txt = text.strip()
    txt = txt.replace(",", ".")
    return float(txt)


def parseIntNumber(text):
    txt = text.strip()
    return int(txt)


def parseLinkHotel(text):
    link = "{}/{}".format(DOMAIN_HOTEL, text)
    print("link: ", link)
    short_link = make_shorten(link)
    return short_link


def parsePrice(text):
    txt = re.sub('[^0-9]', '', text)
    txt = parseIntNumber(txt)
    return txt


def parseNumberPeopleRating(text):
    text = text.strip()
    txt = re.sub('[^0-9]', '', text)
    txt = parseIntNumber(txt)
    return txt


def parseImage(link):
    short_link = make_shorten(link)
    return short_link


def parseQualityStar(text):
    if len(text) == 1:
        return int(text)
    else:

        txts = text.split(" ")
        return int(txts[0])


def parseLinkTour(text):
    link = "{}{}".format(DOMAIN_TOUR, text)
    short_link = make_shorten(link)
    return short_link


def parseRatingTour(text):
    return parseFloatNumber(text)


def parseNumberPeopleRatingTour(text):
    return parseIntNumber(text)


def parseTourId(text):
    return text.split(":")[-1]


class HotelCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pre-processing after get value text
    hotel_name = Field(input_processor=MapCompose(
        str.strip), output_processor=TakeFirst())
    hotel_id = Field(input_processor=MapCompose(
        str.strip), output_processor=TakeFirst())
    address = Field(input_processor=MapCompose(
        str.strip), output_processor=TakeFirst())
    link = Field(input_processor=MapCompose(
        parseLinkHotel), output_processor=TakeFirst())
    quality_star = Field(input_processor=MapCompose(
        parseQualityStar), output_processor=TakeFirst())
    rating = Field(input_processor=MapCompose(
        parseFloatNumber), output_processor=TakeFirst())
    number_people_rating = Field(input_processor=MapCompose(
        parseNumberPeopleRating), output_processor=TakeFirst())
    description = Field(input_processor=MapCompose(
        str.strip), output_processor=TakeFirst())
    distance = Field(input_processor=MapCompose(
        parseDistance), output_processor=TakeFirst())
    image = Field(input_processor=MapCompose(
        parseImage), output_processor=TakeFirst())
    price = Field(input_processor=MapCompose(
        parsePrice), output_processor=TakeFirst())
    city_id = Field(input_processor=MapCompose(
        str.strip), output_processor=TakeFirst())
    pass


class TourItem(scrapy.Item):

    tour_name = Field(input_processor=MapCompose(
        str.strip), output_processor=TakeFirst())
    link = Field(input_processor=MapCompose(
        parseLinkTour), output_processor=TakeFirst())
    rating = Field(input_processor=MapCompose(
        parseRatingTour), output_processor=TakeFirst())
    city_id = Field(input_processor=MapCompose(
        str.strip), output_processor=TakeFirst())
    number_people_rating = Field(input_processor=MapCompose(
        parseNumberPeopleRatingTour), output_processor=TakeFirst())

    image = Field(input_processor=MapCompose(
        parseImage), output_processor=TakeFirst())
    price = Field(input_processor=MapCompose(
        parsePrice), output_processor=TakeFirst())
    start_date = Field(input_processor=MapCompose(
        str.strip), output_processor=TakeFirst())
    start_hour = Field(input_processor=MapCompose(
        str.strip), output_processor=TakeFirst())
    number_available_seat = Field(input_processor=MapCompose(
        parseIntNumber), output_processor=TakeFirst())
    number_days = Field(input_processor=MapCompose(
        parseIntNumber), output_processor=TakeFirst())

    tour_id = Field(input_processor=MapCompose(
        parseTourId), output_processor=TakeFirst())
    pass
