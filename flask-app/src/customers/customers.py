from flask import Blueprint, request, jsonify, make_response
import json
from src import db


customers = Blueprint('customers', __name__)

# Get all customers from the DB
@customers.route('/customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT id, company, last_name, first_name, job_title, business_phone FROM customers')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get customer detail for customer with particular userID
@customers.route('/customers/<userID>', methods=['GET'])
def get_customer(userID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from customers where id = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Update customer information
@customers.route('/customers/<userID>', methods=['PUT'])
def update_customer(userID):
    data = request.json
    if 'company' not in data or 'last_name' not in data or 'first_name' not in data or 'job_title' not in data or 'business_phone' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    cursor = db.get_db().cursor()
    cursor.execute('UPDATE customers SET company = %s, last_name = %s, first_name = %s, job_title = %s, business_phone = %s WHERE id = %s',
                   (data['company'], data['last_name'], data['first_name'], data['job_title'], data['business_phone'], customer_id))
    db.get_db().commit()
    cursor.execute('SELECT id, company, last_name, first_name, job_title, business_phone FROM customers WHERE id = %s', (customer_id,))
    row_headers = [x[0] for x in cursor.description]
    updated_customer = dict(zip(row_headers, cursor.fetchone()))
    return jsonify(updated_customer), 200        