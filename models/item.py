"""
item class: get the item price from the website and save to database
"""

import re
import uuid
from dataclasses import dataclass, field
from typing import Dict
import requests
from bs4 import BeautifulSoup
from models.model import Model


@dataclass(eq=False)  # we can compare the items
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def load_price(self) -> float:
        response = requests.get(self.url)  # get url
        content = response.content  # content of the page
        soup = BeautifulSoup(content, 'html.parser')  # tell the content is html, tell soup read the html we've received, use html parser for that content
        element = soup.find(self.tag_name, self.query)  # find element matches our search, find element has P tag and class
        string_price = element.text.strip()  # get text of element, strip()--remove the white space

        pattern = re.compile(r"(\d+,?\d+\.\d+)")  # \d means a number, ? is an optional thing in string, * is zero or more number
        match = pattern.search(string_price)
        found_price = match.group(1)
        without_comma = found_price.replace(',', '')
        self.price = float(without_comma)
        return self.price

    def json(self) -> Dict:
        """
        need a method turns item from python object to store in mongodb(dict)
        :return:
        """
        return {
            '_id': self._id,
            'url': self.url,
            'tag_name': self.tag_name,
            'price': self.price,
            'query': self.query
        }


"""
    @property
    def id(self):
        return self._id
"""