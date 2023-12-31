from datetime import datetime

from flask_restful.representations import json
from google.cloud import firestore
from flask import request
from flask_restful import Resource, reqparse
from app.api.models.Bill import Bill
from firebase_admin import firestore

db = firestore.client()

# Create Bill:
# POST /bills: This endpoint creates a new bill.

# Retrieve Bill
# GET /bills/{bill_id}: Retrieve a specific bill by its ID.
# GET /bills/diner/{diner_id}: Retrieve bills for a specific diner.
# GET /bills/workshift/{workshift_id}: Retrieve bills for a specific workshift.

# Update Bill:
# PUT /bills/{bill_id}: Update the status or details of a specific bill.

# Delete Bill:
# DELETE /bills/{bill_id}: Delete a specific bill by its ID.


class BillDetailResource(Resource):
    def get(self, bill_id):
        # Retrieve a specific bill by ID
        bill = Bill.get_bill_by_id(bill_id)
        if bill:
            return bill.to_dict(), 201
        return {"message": "Bill not found"}, 404

    def put(self, bill_id):
        # Update an existing bill by ID
        data = request.get_json()
        bill = Bill.get_bill_by_id(bill_id)
        if bill:
            bill.update_attributes(data)
            return {"message": "Bill updated successfully"}, 201
        return {"message": "Bill not found"}, 404

    def delete(self, bill_id):
        # Delete a bill by ID
        bill = Bill.get_bill_by_id(bill_id)
        if bill:
            bill.delete_from_db()
            return {"message": "Bill deleted successfully"}, 201
        return {"message": "Bill not found"}, 404


class BillResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('bill_id', type=str)
        self.parser.add_argument('diner_id', type=str)
        self.parser.add_argument('table_id', type=str)
        self.parser.add_argument('order_ids', type=list, default=[])
        self.parser.add_argument('total_price', type=float, default=0.0)
        self.parser.add_argument('payment_method', type=str, default="")
        self.parser.add_argument('payment_status', type=str, default="Unpaid")
        self.parser.add_argument('shift', type=datetime, default=datetime.now())

    def post(self):
        args = self.parser.parse_args()
        args['shift'] = firestore.SERVER_TIMESTAMP
        bill = Bill(**args)
        bill.save()
        return {"message": "Bill created successfully"}, 201

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

        return {"bills": [bill.to_dict() for bill in filtered_bills]}, 200
