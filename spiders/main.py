from pathlib import Path
import scrapy
import datetime
from pymongo import MongoClient
MONGO_URI = "mongodb_url"
client = MongoClient(MONGO_URI)

db = client.IMDB

def insertData(title,image,year,duration,rating,metascore,description,votescore):
    collection = db["Top100Movies"]
    object = {
    "title": title,
    "src": image,
    "year": year,
    "duration": duration,
    "rating": rating,
    "metascore": metascore,
    "votescore": votescore,
    "description": description,
    "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }
    post_id = collection.insert_one(object)


class QuotesSpider(scrapy.Spider):
    name = "main"

    def start_requests(self):
        urls = [
            "https://www.imdb.com/search/title/?groups=top_100&sort=user_rating,desc"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        cards=response.css(".sc-74bf520e-3")
        for card in cards:
            image=card.css(".ipc-image").attrib["src"]
            title=card.css(".ipc-title__text::text").get()
            year=card.css(".sc-b189961a-8::text")[0].get()
            duration=card.css(".dli-title-metadata-item::text")[1].get()
            rating=card.css(".ipc-rating-star").attrib["aria-label"].split(":")[1]
            metascore=card.css(".metacritic-score-box::text").get()
            description=card.css(".ipc-html-content-inner-div::text").get()
            votescore=card.css(".ipc-rating-star--voteCount").get().split('<span class="ipc-rating-star--voteCount">')[1].split('\xa0(<!-- -->')[1].split("<!-- -->)</span>")[0]
            insertData(title,image,year,duration,rating,metascore,description,votescore)
        