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
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
listings = Blueprint('listings', __name__)


#------------------------------------------------------------
# Get all listings
@listings.route('/listings', methods=['GET'])
def get_listings():

    cursor = db.get_db().cursor()
    cursor.execute('''
                    SELECT * FROM listings
    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Add a new listing
@listings.route('/listings', methods=['POST'])
def add_listing():
    current_app.logger.info('PUT /listings route')
    listing_info = request.json
    rent_amount = listing_info['rent_amount']
    title = listing_info['title']
    description = listing_info['description']
    amenities = listing_info['amenities']
    safety_rating = listing_info['safety_rating']
    location = listing_info['location']
    created_by = listing_info['created_by']
    neighborhood_id = listing_info['neighborhood_id']
    house_number = listing_info['house_number']
    street = listing_info['street']
    city = listing_info['city']
    zipcode = listing_info['zipcode']
    verification_status = listing_info['verification_status']
    timeline = listing_info['timeline']

    query = '''
        INSERT INTO listings (rent_amount, title, description, amenities, match_score, safety_rating, location, created_by, neighborhood_id, house_number, street, city, zipcode, verification_status, timeline)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    data = (rent_amount, title, description, amenities, safety_rating, location, created_by, neighborhood_id, house_number, street, city, zipcode, verification_status, timeline)

    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()

    the_response = make_response(jsonify('listing added!'))
    the_response.status_code = 201

    return the_response

# Get a listing by ID
@listings.route('/listings/<listingID>', methods=['GET'])
def get_listing(listingID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                    SELECT * FROM listings WHERE listing_id = %s
    ''', (listingID,))
    
    theData = cursor.fetchall()
    
    if theData:
        the_response = make_response(jsonify(theData))
        the_response.status_code = 200
    else:
        the_response = make_response(jsonify({'error': 'Listing not found'}))
        the_response.status_code = 404
    
    return the_response

# Update a listing by ID
@listings.route('/listings/<listingID>', methods=['PUT'])
def update_listing(listingID):
    current_app.logger.info('PUT /listings/<listingID> route')
    listing_info = request.json
    rent_amount = listing_info['rent_amount']
    title = listing_info['title']
    description = listing_info['description']
    amenities = listing_info['amenities']
    safety_rating = listing_info['safety_rating']
    location = listing_info['location']
    neighborhood_id = listing_info['neighborhood_id']
    house_number = listing_info['house_number']
    street = listing_info['street']
    city = listing_info['city']
    zipcode = listing_info['zipcode']
    verification_status = listing_info['verification_status']
    timeline = listing_info['timeline']

    query = '''
        UPDATE listings SET rent_amount = %s, title = %s, description = %s, amenities = %s, safety_rating = %s, location = %s, neighborhood_id = %s, house_number = %s, street = %s, city = %s, zipcode = %s, verification_status = %s, timeline = %s
        WHERE listing_id = %s
    '''
    data = (rent_amount, title, description, amenities, safety_rating, location, neighborhood_id, house_number, street, city, zipcode, verification_status, timeline, listingID)

    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()

    the_response = make_response(jsonify('listing updated!'))
    the_response.status_code = 200
    return the_response

# Delete a listing by ID
@listings.route('/listings/<listingID>', methods=['DELETE'])
def delete_listing(listing_id):
    query = '''
        DELETE FROM listings WHERE listing_id = %s
    '''
    data = (listing_id)

    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()

    the_response = make_response(jsonify('listing deleted!'))
    the_response.status_code = 200
    return the_response

# Get all listings created in the last 7 days
@listings.route('/listings/new', methods=['GET'])
def get_new_listings():
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT 
                   rent_amount, 
                   title, 
                   description, 
                   amenities, 
                   match_score, 
                   safety_rating, 
                   location, 
                   created_by, 
                   neighborhood_id, 
                   house_number, 
                   street, 
                   city, 
                   zipcode, 
                   verification_status, 
                   timeline 
                   FROM listings 
                   WHERE created_at >= DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 7 DAY);

    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Approve a specific listing
@listings.route('/listings/approve/<listingID>', methods=['PUT'])
def approve_listing(listing_id):
    query = '''
        UPDATE listings SET verification_status = TRUE WHERE listing_id = %s
    '''
    data = (listing_id)

    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()

    the_response = make_response(jsonify('listing approved!'))
    the_response.status_code = 200
    return the_response

# Deny a specific listing
@listings.route('/listings/deny/<listingID>', methods=['PUT'])
def deny_listing(listing_id):
    query = '''
        UPDATE listings SET verification_status = FALSE WHERE listing_id = %s
    '''
    data = (listing_id)

    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()

    the_response = make_response(jsonify('listing denied!'))
    the_response.status_code = 200
    return the_response

# Get a listing based on filters
@listings.route('/listings/filter', methods=['GET'])
def filter_listings():
    current_app.logger.info('GET /listings/filter route')
    listing_info = request.json
    rent_amount = listing_info['rent_amount']
    title = listing_info['title']
    description = listing_info['description']
    amenities = listing_info['amenities']
    safety_rating = listing_info['safety_rating']
    location = listing_info['location']
    created_by = listing_info['created_by']
    neighborhood_id = listing_info['neighborhood_id']
    house_number = listing_info['house_number']
    street = listing_info['street']
    city = listing_info['city']
    zipcode = listing_info['zipcode']
    verification_status = listing_info['verification_status']
    timeline = listing_info['timeline']

    query = '''
        SELECT * FROM listings WHERE rent_amount = %s AND title = %s AND description = %s AND amenities = %s AND safety_rating = %s AND location = %s AND created_by = %s AND neighborhood_id = %s AND house_number = %s AND street = %s AND city = %s AND zipcode = %s AND verification_status = %s AND timeline = %s
    '''
    data = (rent_amount, title, description, amenities, safety_rating, location, created_by, neighborhood_id, house_number, street, city, zipcode, verification_status, timeline)

    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()

    the_response = make_response(jsonify('listing filtered!'))
    the_response.status_code = 200
    return the_response