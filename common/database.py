import os
from typing import Dict

import pymongo as pymongo


class Database:
    URI = os.environ.get("MONGOLAB_URI")  # port of mongodb
    DATABASE = pymongo.MongoClient(URI).get_default_database()  # get database

    @staticmethod  # call method directly with class(Database), without creating a object of the class
    def insert(collection: str, data: Dict):
        Database.DATABASE[collection].insert(data)  # take any data, put in any collection

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:
        # query is going to match what we search for in mongodb{'_id':'123'}
        # cursor is an iterable, like a list(can use for loop)

        return Database.DATABASE[collection].find(query)  # call lib find element in this collection with this query

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].find_one(query)  # the collection object in pymongo has these properties

    @staticmethod
    def update(collection: str, query: Dict, data: Dict) -> None:
        """
        everything matches the query, content of that thing will replaced by the data
        :param collection: items
        :param query: query match things want to update
        :param data: new data
        """
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].remove(query)