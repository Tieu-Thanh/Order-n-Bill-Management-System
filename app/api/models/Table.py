from . import db


class Table:
    def __init__(self, table_id, capacity, status):
        self.table_id = table_id
        self.capacity = capacity
        self.status = status
        self.booked_by = ""
        # self.bills = []

    def to_dict(self):
        return {
            'table_id': self.table_id,
            'capacity': self.capacity,
            'status': self.status,
            'booked_by': self.booked_by
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['table_id'],
            data['capacity'],
            data['status']
        )
    @classmethod
    def get_tables(cls):
        table_ref = db.collection('tables')
        tables = table_ref.stream()
        return [cls.from_dict(table.to_dict()) for table in tables]

    @classmethod
    def get_table_by_id(cls, table_id):
        table_ref = db.collection('tables').document(table_id)
        table_doc = table_ref.get()
        if table_doc is None:
            return {'message': 'Table not found'}, 404

        table = table_doc.to_dict()
        return table

    def save(self):
        table_ref = db.collection('tables').document(self.table_id)
        table_ref.set(self.to_dict())

    def delete(self):
        table_ref = db.collection('tables').document(self.table_id)
        table_ref.delete()

    def book_table(self, diner_id):
        if self.status == "available":
            self.status = "booked"
            self.booked_by = diner_id
            self.save()
            return True
        return False
