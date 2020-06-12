import uuid
import re
from dataclasses import dataclass, field
from typing import Dict

from models.model import Model


@dataclass(eq=False)
class Store(Model):
    collection: str = field(init=False, default="stores")
    name: str
    url_prefix: str
    tag_name: str
    query: Dict
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_name(cls, store_name: str) -> "Store":  # Store.get_by_name('John Lewis')
        return cls.find_one_by("name", store_name)

    @classmethod
    def get_by_url_prefix(cls, url_prefix: str) -> "Store":  # Store.get_by_url_prefix('http://www.163.com')start with
        """
        going to take in a url prefix and will match a store and its gonna search the database for that
        :param url_prefix:  prefix of the whole url
        :return: url
        """
        url_regex = {"$regex": '^{}'.format(url_prefix)}  # passing $regex database will treat ^{}.format(url_prefix)
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url: str):
        """
        take in a item url, return a store from a url like "http://www.johnlewis.com/item/sdfj4h5g4g21k.html"
        we can find a store in database when we only have partial information of an item url(http://www.johnlewis.com/)
        :param url: the item's url
        :return: a store
        """
        pattern = re.compile(r"(https?:\/\/.*?\/)")  # correctly match https://www.johnlewis.com/
        match = pattern.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)
