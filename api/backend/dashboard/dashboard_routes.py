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

# Create a new Blueprint for Dashboard
dashboard = Blueprint('dashboard', __name__)

# Retrieve all dashboard
@dashboard.route('/dashboard', methods=['GET'])
def get_all_dashboard():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM analyticsDashboard')
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# Get a dashboard by ID
@dashboard.route('dashboard/<int:dashboard_id>', methods=['GET'])
def get_dashboard(dashboard_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
                    SELECT * FROM analyticsDashboard WHERE dashboard_id = {0}
    '''.format(dashboard_id))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Add a new dashboard
@dashboard.route('dashboard/<int:dashboard_id>', methods=['POST'])
def add_dashboard():
    current_app.logger.info('POST /dashboard route')
    dashboard_info = request.json
    seasonal_trend = dashboard_info['seasonal_trend']
    vacancy_rate = dashboard_info['vacancy_rate']
    safety_flag = dashboard_info['safety_flag']
    demand_forecast = dashboard_info['demand_forecast']
    neighborhood = dashboard_info['neighborhood']

    query = '''
        INSERT INTO listings (seasonal_trend, vacancy_rate, safety_flag, demand_forecast, neighborhood)
        VALUES (%s, %s, %s, %s, %s)
    '''
    data = (seasonal_trend, vacancy_rate, safety_flag, demand_forecast, neighborhood)

    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()

    the_response = make_response(jsonify('listing added!'))
    the_response.status_code = 201

    return the_response

# Update an existing dashboard by ID
@dashboard.route('/dashboard/<int:dashboard_id>', methods=['PUT'])
def update_dashboard(dashboard_id):
    current_app.logger.info(f'PUT /dashboard/{dashboard_id} route')
    dashboard_info = request.json
    seasonal_trend = dashboard_info.get('seasonal_trend', None)
    vacancy_rate = dashboard_info.get('vacancy_rate', None)
    safety_flag = dashboard_info.get('safety_flag', None)
    demand_forecast = dashboard_info.get('demand_forecast', None)
    neighborhood = dashboard_info.get('neighborhood', None)
    
    query = '''
        UPDATE dashboard
        SET seasonal_trend = %s, vacancy_rate = %s, safety_flag = %s, demand_forecast = %s, neighborhood = %s
        WHERE dashboard_id = %s
    '''

    data = (seasonal_trend, vacancy_rate, safety_flag, demand_forecast, neighborhood, dashboard_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()

    response = make_response(jsonify({'message': 'Dashboard updated successfully!'}))
    response.status_code = 200
    return response

# Delete a dashboard by ID
@dashboard.route('/dashboard/<int:dashboard_id>', methods=['DELETE'])
def delete_dashboard(dashboard_id):
    query = 'DELETE FROM dashboard WHERE dashboard_id = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (dashboard_id,))
    db.get_db().commit()
    
    response = make_response(jsonify({'message': 'Dashboard deleted successfully!'}))
    response.status_code = 200
    return response

