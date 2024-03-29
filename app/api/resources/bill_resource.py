from datetime import datetime

from flask_restful.representations import json
from google.cloud import firestore
from flask import request
from flask_restful import Resource, reqparse
from app.api.models.Bill import Bill
from app.api.models.Order import Order
from firebase_admin import firestore

db = firestore.client()


class BillDetailResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('payment_status', type=str, help="Payment")
        self.parser.add_argument('payment_method', type=str, help="Payment method")
        self.parser.add_argument('table_id', type=str, help="New table id")

    def get(self, bill_id):
        # Retrieve bill and associated orders
        bill = Bill.get_bill_by_id(bill_id)
        if bill:
            try:
                return {'bill': bill.to_dict()}, 201

            except Exception as e:
                return {"message": f"Error retrieving order details: {e}"}, 500

        return {"message": "Bill not found"}, 404

    def put(self, bill_id):
        # Update an existing bill by ID
        args = parser.parse_args()
        bill = Bill.get_bill_by_id(bill_id)
        if bill:
            bill.update_attributes(**args)
            return {"message": "Bill updated successfully"}, 201
        return {"message": "Bill not found"}, 404

    def delete(self, bill_id):
        # Delete a bill by ID
        bill = Bill.get_bill_by_id(bill_id)
        if bill:
            bill.delete_from_db()
            return {"message": "Bill deleted successfully"}, 201
        return {"message": "Bill not found"}, 404

    def patch(self, bill_id):
        bill = Bill.get_bill_by_id(bill_id)
        if not bill:
            return {"message": "Bill not found"}, 404

        args = self.parser.parse_args()
        new_table_id = args["table_id"]
        if new_table_id:
            bill.change_table(new_table_id)
            return {'message': 'Bill updated successfully'}, 201

        return {"message": "Table_id not found"}, 404

class BillResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('bill_id', type=str)
        self.parser.add_argument('diner_id', type=str)
        self.parser.add_argument('table_id', type=str)

    def post(self):
        args = self.parser.parse_args()
        bill = Bill(**args)
        bill.save()
        bill.calculate_total_price()
        return {"message": "Bill created successfully",
                "bill": bill.to_dict()}, 201

    def get(self):
        filter_param = {}
        sort_field = request.args.get('sort_by')
        sort_order = request.args.get('sort', 'asc').lower()

        # Extract filtering parameters from request.args, ensuring data integrity
        allowed_fields = ['bill_id', 'diner_id', 'table_id', 'payment_status',
                          'other_valid_fields']  # Add more fields as needed
        for field in allowed_fields:
            value = request.args.get(field)
            if value:
                try:
                    # Validate values if necessary (e.g., for numbers, dates)
                    filter_param[field] = value
                except ValueError:
                    return {"error": f"Invalid value for field '{field}'"}, 400

        # Retrieve filtered and sorted bills
        filtered_bills = Bill.filter_bills(filter_param, sort_field, sort_order)

        return {"bills": [bill.to_dict() for bill in filtered_bills]}, 201

    # def get(self):
    #     bills = Bill.get_bills()
    #     return {"bills": [bill.to_dict() for bill in bills]}, 200