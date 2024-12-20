########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

# Create a new Blueprint for neighborhoods
neighborhoods = Blueprint('neighborhoods', __name__)

# Retrieve all neighborhoods
@neighborhoods.route('/neighborhoods', methods=['GET'])
def get_all_neighborhoods():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM neighborhoods')
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# Retrieve neighborhoods by name
@neighborhoods.route('/neighborhoods/<name>', methods=['GET'])
def get_zipcode_event(name):
    cursor = db.get_db().cursor()
    query = 'SELECT * FROM neighborhoods WHERE name = %s'
    cursor.execute(query, (name,))
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response


# Add a new neighborhood
@neighborhoods.route('/neighborhoods', methods=['POST'])
def add_neighborhood():
    current_app.logger.info('POST /neighborhoods route')
    neighborhood_info = request.json
    name = neighborhood_info['name']
    population_density = neighborhood_info.get('population_density', None)
    safety_travel = neighborhood_info.get('safety_travel', None)
    insights = neighborhood_info.get('insights', None)
    
    query = '''
        INSERT INTO neighborhoods (name, zipcode, population_density, safety_travel, insights)
        VALUES (%s, %s, %s, %s, %s)
    '''
    data = (name, population_density, safety_travel, insights)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Neighborhood added successfully!'}))
    response.status_code = 201
    return response

# Update an existing neighborhood by ID
@neighborhoods.route('/neighborhoods/<int:neighborhood_id>', methods=['PUT'])
def update_neighborhood(neighborhood_id):
    current_app.logger.info(f'PUT /neighborhoods/{neighborhood_id} route')
    neighborhood_info = request.json
    name = neighborhood_info.get('name', None)
    population_density = neighborhood_info.get('population_density', None)
    safety_travel = neighborhood_info.get('safety_travel', None)
    insights = neighborhood_info.get('insights', None)
    
    query = '''
        UPDATE neighborhoods
        SET name = %s, population_density = %s, safety_travel = %s, insights = %s
        WHERE neighborhood_id = %s
    '''

    data = (name, population_density, safety_travel, insights, neighborhood_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()

    response = make_response(jsonify({'message': 'Neighborhood updated successfully!'}))
    response.status_code = 200
    return response

# Delete a neighborhood by ID
@neighborhoods.route('/neighborhoods/<int:neighborhood_id>', methods=['DELETE'])
def delete_neighborhood(neighborhood_id):
    query = 'DELETE FROM neighborhoods WHERE neighborhood_id = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (neighborhood_id,))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Neighborhood deleted successfully!'}))
    response.status_code = 200
    return response