"""
model class: contain the duplicate method in alerts and item class
"""

from typing import List, TypeVar, Type, Dict, Union
from common.database import Database
from abc import ABCMeta, abstractmethod

T = TypeVar('T', bound='Model')

"""
# 多态性是指具有不同功能的函数可以使用相同的函数名，这样就可以用一个函数名调用不同内容的函数。
# 在面向对象方法中一般是这样表述多态性：向不同的对象发送同一条消息，不同的对象在接收时会产生不同的行为（即方法）
# 。也就是说，每个对象可以用自己的方式去响应共同的消息。所谓消息，就是调用函数，不同的行为就是指不同的实现，即执行不同的函数。
# 上述代码子类是约定俗称的实现这个方法，加上@abc.abstractmethod装饰器后严格控制子类必须实现这个方法
"""


class Model(metaclass=ABCMeta):  # inherit from ABCMeta, to use metaclass inheritance, give this class ability to use abstract property
    """
    多态，同一事物，子类可以实现，并以不同方式实现
    give class ability to use abstract method or property, abstract--exists but isn't defined yet
    all model has json, save_to_mongo, etc.
    """
    collection: str
    _id: str  # exist but we don't have value yet

    def __init__(self, *arts, **kwargs):
        pass

    def save_to_mongo(self):
        """
        update is insert new things in database unless there is already sth in database matching the _id
        :return:
        """
        Database.update(self.collection, {"_id": self._id}, self.json())

    def remove_from_mongo(self):
        Database.remove(self.collection, {"_id": self._id})

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T:  # item.get_by_id()-> item, alerts->alerts
        # return cls(**Database.find_one(cls.collection, {'_id': _id}))
        return cls.find_one_by('_id', _id)

    @abstractmethod
    def json(self) -> Dict:
        """
        we have a model class, but isn't actual thing of program, it's the definition of what a thing should be
        models in app should contain json
        now going to any model create a class, it can inherit from model abstract class
        """
        raise NotImplementedError  # child class must implement this method(json()), but in different ways

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        """
        give a list of item objects
        cls is the current class, cls is equal to Item class
        **item is passing four arguments:_id, url, tag, query, because the parameters has the same as the keys in json
        """
        # pymongo cursor, find return a cursor, can iterate by for loop
        elements_from_db = Database.find(cls.collection, {})
        # iterate the items_from_db so the item is each of the dicts in that cursor
        # return [Item(_id=item['_id'], url=item['url']) for item in items_from_db], given a list of item objects
        return [cls(**elem) for elem in elements_from_db]

    @classmethod
    def find_one_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> T:  # Item.find_one_by('url', 'http://12321s.com')
        return cls(**Database.find_one(cls.collection, {attribute: value}))  # ** is named arguments

    @classmethod
    def find_many_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> List[T]:
        return [cls(**elem) for elem in Database.find(cls.collection, {attribute: value})]



