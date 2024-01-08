from . import db


class Table:
    def __init__(self, table_id, capacity, status):
        self.table_id = table_id
        self.capacity = capacity
        self.status = status
        self.bills = []

