import scrapy
from scrapy.loader import ItemLoader
from hotel_crawl.items import HotelCrawlItem, TourItem
from hotel_crawl.constant import LIST_ID_CITY, LIST_TOUR
from scrapy import Request
from scrapy.selector import Selector
import pdb
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import html
from time import sleep
from hotel_crawl.spiders.selenium_html import SeleniumHtmlGetter

html_getter = SeleniumHtmlGetter()


class TourSpider(scrapy.Spider):
    name = "tour"
    allowed_domains = ["travel.com.vn"]
    start_urls = ["https://travel.com.vn"]

    def parse(self, response, **kwargs):
        for key in LIST_TOUR:
            link = LIST_TOUR[key]
            html_tree = html_getter.get_html(link)
            tour_items = self.parse_tour(html_tree, city_id=key)
            if tour_items and len(tour_items) > 0:
                for tour_item in tour_items:
                    yield tour_item.load_item()
        pass

    def parse_tour(self, html, city_id):
        tour_items = []
        scrapy_selector = Selector(text=html)
        tours = scrapy_selector.xpath(
            "//div[@class='col-lg-11 col-md-11 col-sm-12 col-xs-12']")
        if tours is not None and len(tours) > 0:
            for index, tour in enumerate(tours):
                tour_selector_text = tour.get()
                tour_selector = Selector(text=tour_selector_text)
                loader = ItemLoader(item=TourItem(),
                                    selector=tour_selector)
                loader.add_value("city_id", city_id)
                # pdb.set_trace()
                # get tourname
                loader.add_xpath(
                    "tour_name", "//div[@class='tour-name']/a/h3/text()")

                # get tour link
                loader.add_xpath("link", "//div[@class='tour-name']/a/@href")

                # get rating
                rating_path = tour_selector.xpath(
                    "//span[@class='average']/strong/text()")
                if len(rating_path) > 0:

                    loader.add_xpath(
                        "rating", "//span[@class='average']/strong/text()")
                else:
                    loader.add_value("rating", ["0.0"])

                # get number rating
                number_people_rating_path = tour_selector.xpath(
                    "//span[@class='votes']/strong/text()")
                if len(number_people_rating_path) > 0:

                    loader.add_xpath(
                        "number_people_rating", "//span[@class='votes']/strong/text()")
                else:
                    loader.add_value("number_people_rating", ["0"])

                # get image
                loader.add_xpath(
                    "image", "//img[@class='img-responsive pic-lt']/@src")

                # get price
                loader.add_xpath(
                    "price", "//span[@class='font500 price']/text()")

                # get start_date
                loader.add_xpath("start_date",
                                 "//div[@class='col-md-7 col-sm-7 col-xs-12 mg-bot10']/div[2]/span[@class='font500']/text()")

                # get tour_id

                tour_id_path = tour_selector.xpath(
                    "//div[@class='col-md-7 col-sm-7 col-xs-12 mg-bot10']/div[2]/text()")[0]
                loader.add_value("tour_id", tour_id_path.get())

                # get start_hour, number_available_seat
                paths = tour_selector.xpath(
                    "//div[@class='col-md-5 col-sm-5 col-xs-12 mg-bot10']/div[2]/span/text()")
                keys = ["number_available_seat", "start_hour"]
                for index, path in enumerate(paths):
                    loader.add_value(keys[index], path.get())
                # get number_days
                loader.add_xpath(
                    "number_days", "//div[@class='col-md-5 col-sm-5 col-xs-12']/div[2]/span/text()")
                tour_items.append(loader)
        return tour_items
