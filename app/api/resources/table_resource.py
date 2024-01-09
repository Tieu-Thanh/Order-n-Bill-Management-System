from flask_restful import Resource, reqparse
from flask import request
from app.api.models.Table import Table

class TableResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('table_id', type=str, required=True)
        self.parser.add_argument('capacity', type=int, required=True)

    def get(self):
        tables = Table.get_tables()
        return {'tables': [table.to_dict() for table in tables]}, 200

    def post(self):
        args = self.parser.parse_args()
        table_id = args['table_id']
        capacity = args['capacity']

        new_table = Table(table_id, capacity, "available")  # Initialize a new table
        new_table.save()  # Save the new table to Firestore
        return {'message': f'Table {table_id} created successfully'}, 201

    def delete(self):
        args = self.parser.parse_args()
        table_id = args['table_id']

        table = Table.get_table_by_id(table_id)
        if table:
            table.delete_from_db()  # Delete the specified table
            return {'message': f'Table {table_id} deleted successfully'}, 200

        return {'message': f'Table {table_id} not found'}, 404

class TableDetailResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('table_id', type=str, required=True)

    def patch(self, table_id):
        args = self.parser.parse_args()
        diner_id = args['diner_id']

        table = Table.get_table_by_id(table_id)
        if table and table.book_table(diner_id):
            return {'message': f'Table {table_id} booked successfully'}, 200

        return {'message': 'Failed to book table'}, 400