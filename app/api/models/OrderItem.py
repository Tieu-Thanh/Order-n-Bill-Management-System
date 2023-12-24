from . import db


class OrderItem:
    def __init__(self, menu_item_id, quantity, special_request, status="pending", amount=None):
        self.__menu_item_id = menu_item_id
        self.__name = None
        self.__quantity = quantity
        self.__special_request = special_request
        self.__status = status
        self.__amount = self.__calculate_total()

    def to_dict(self):
        self.__set_name()
        self.__calculate_total()  # update amount before serialization.
        return {
            'menu_item_id': self.__menu_item_id,
            'name': self.get_name(),
            'quantity': self.__quantity,
            'special_request': self.__special_request,
            'amount': self.__amount,
            'status': self.__status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            menu_item_id=data.get('menu_item_id'),
            quantity=data.get('quantity'),
            special_request=data.get('special_request'),
            status=data.get('status'),
            amount=data.get('amount')
        )

    def __calculate_total(self):
        menu_doc = db.collection('menu_items').document(self.__menu_item_id).get()
        menu_item_price = menu_doc.to_dict()['price']
        return menu_item_price * self.__quantity

    def __set_name(self):
        if not self.__name: # if Name is not cached
            menu_doc = db.collection('menu_items').document(self.__menu_item_id).get()
            self.__name = menu_doc.to_dict()['name']
        return self.__name

    def get_amount(self):
        return self.__amount

    def get_name(self):
        return self.__name

    def save(self, order_id):
        order_items_ref = db.collection('orders').document(order_id).collection('order_items')
        order_items_ref.document(self.__menu_item_id).set(self.to_dict())

    def update_status(self, new_status, order_id):
        self.__status = new_status
        self.save(order_id)  # Persist the updated status to Firestore

    @classmethod
    def get_by_id(cls, order_id, menu_item_id):
        order_items_ref = db.collection('orders').document(order_id).collection('order_items')
        order_item_doc = order_items_ref.document(menu_item_id).get()
        if order_item_doc.exists:
            return cls.from_dict(order_item_doc.to_dict())
        else:
            return None
