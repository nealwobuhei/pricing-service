"""
alerts user when item current price is lower than alerts price
"""

import uuid
from typing import Dict
from dataclasses import dataclass, field

from libs.mailgun import Mailgun
from models.item import Item
from models.user import User
from models.model import Model


@dataclass(eq=False)  # to remove all equality generation from our dataclass
class Alert(Model):
    collection: str = field(init=False, default='alerts')  # tell data class about collection, can't be modified, 'alerts' is it's value
    name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        """
        run after __init__ method, can access self., you've got above value s stored in self, you can do self.item_id
        """
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        """
        have all of the things we want to save in mongodb as alerts
        :return: Dict of information
        """

        return {
            '_id': self._id,
            "name": self.name,
            'price_limit': self.price_limit,
            'item_id': self.item_id,
            'user_email': self.user_email
        }

    def load_item_price(self):
        self.item.load_price()  # benefits, having item objects let us call the method, don't have to rewrite, get price in item model
        return self.item.price

    def notify_if_price_reached(self) -> None:
        if self.item.price < self.price_limit:
            print(f"Item {self.item} has reached a price under {self.price_limit}. Latest price: {self.item.price}.")
            Mailgun.send_email(
                email=[self.user_email],
                subject=f"Notification for {self.name}",
                text=f"Your alert {self.name} has reached a price under {self.price_limit}. The latest price is {self.item.price}. Go to this address to check your item: {self.item.url}.",
                html=f'<p>Your alert {self.name} has reached a price under {self.price_limit}.</p><p>The latest price is {self.item.price}. Check your item out <a href="{self.item.url}>here</a>.</p>',
            )