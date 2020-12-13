# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from hotel_crawl.models import create_table, db_connect, Tour, Hotel
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem


class TourCrawPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
        pass

    def process_item(self, item, spider):
        """Save hotels in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        tour = Tour()
        tour.tour_name = item["tour_name"]
        tour.link = item["link"]
        tour.city_id = item["city_id"]
        tour.rating = item["rating"]
        tour.number_people_rating = item["number_people_rating"]
        tour.image = item["image"]
        tour.price = item["price"]
        tour.tour_id = item["tour_id"]
        tour.start_date = item["start_date"]
        tour.start_hour = item["start_hour"]
        tour.number_available_seat = item["number_available_seat"]
        tour.number_days = item["number_days"]
        try:
            session.add(tour)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item


class DuplicatesPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        exist_quote = session.query(Tour).filter_by(
            tour_id=item["tour_id"]).first()
        if exist_quote is not None:  # the current quote exists
            raise DropItem("Duplicate item found: %s" % item["tour_id"])
            session.close()
        else:
            return item
            session.close()
