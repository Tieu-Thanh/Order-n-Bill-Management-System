from . import db


class MenuItem:
    def __init__(self, item_id, name, description, price, is_on_stock=True, category=None, image_url=None):
        self.__item_id = item_id
        self.__name = name
        self.__description = description
        self.__price = price
        self.__is_on_stock = is_on_stock
        self.__category = category
        self.__image_url = image_url

    def get_item_id(self):
        return self.__item_id

    def to_dict(self):
        return {
            "item_id": self.__item_id,
            "name": self.__name,
            "description": self.__description,
            "price": self.__price,
            "is_on_stock": self.__is_on_stock,
            "category": self.__category,
            "image_url": self.__image_url
        }

    @classmethod
    def from_firestore_data(cls, data):
        return cls(
            item_id=data.get('item_id'),
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            is_on_stock=data.get('is_on_stock'),
            category=data.get('category'),
            image_url=data.get('image_url')
        )

    @classmethod
    def save(cls, menu_item):
        menu_ref = db.collection('menu_items')
        query = menu_ref.where('item_id', '==', menu_item.get_item_id()).limit(1).get()
        if any(query):
            return {'error:' f"Item with id {menu_item.get_item_id()} already exists"}, 400
        doc_ref = menu_ref.document(menu_item.get_item_id()).set(menu_item.to_dict())
        return menu_item

    @classmethod
    def list_items(cls):
        menu_ref = db.collection('menu_items')
        menu_items = menu_ref.stream()
        return [cls.from_firestore_data(menu_item) for menu_item in menu_items]

    @classmethod
    def get_item(cls, menu_item_id):
        menu_ref = db.collection('menu_items')
        doc_ref = menu_ref.document(menu_item_id).get()
        if doc_ref.exists:
            menu_item = cls.from_firestore_data(doc_ref.to_dict())
            menu_item.item_id = doc_ref.id
            return menu_item
        else:
            return None

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        menu_ref = db.collection('menu_items')
        menu_ref.document(self.__item_id).update(self.to_dict())

    def delete(self):
        menu_ref = db.collection('menu_items')
        menu_ref.document(self.__item_id).delete()

    @classmethod
    def get_items_by_category(cls, category):
        menu_ref = db.collection('menu_items')
        query = menu_ref.where('category', '==', category).stream()
        return [cls.from_firestore_data(menu_item.to_dict()) for menu_item in query]
