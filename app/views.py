from flask import request, jsonify, make_response, session, logging
import json
from flask_login import LoginManager
from functools import wraps

from app import app

from .models import User
from .models import Business
from .models import Review


business_reviews = []

# Endpoint to Register user and ssaving the details in a list called users


@app.route('/api/v1/auth/register',  methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if username is None:
        return make_response(jsonify({"error": "Missing key"}), 409)
    if type(username) != str:
        return make_response(jsonify({"error": "username cannot be an integer"}), 409)
    if type(email) != str:
        return make_response(jsonify({"error": "email cannot be an integer"}), 409)
    if type(password) != str:
        return make_response(jsonify({"error": "password must be a string data type"}), 409)
    # check if the user details already in the list, otherwise add the details in the list
    available_emails = [user.email for user in User.users]
    if email in available_emails:
        return make_response(jsonify({"message": "Email already taken"}), 409)
    else:
        try:
            user = User.register_user(username, email, password)
        except AssertionError as err:
            return make_response(jsonify({'error': err.args[0]}), 409)

    return make_response(jsonify({"message": "Registration Successful"}), 201)

# Login user


@app.route('/api/v1/auth/login',  methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # check if the user details exist in the list, otherwise deny access.
    if data['username'] == "" or data['password'] == "":
        return make_response(jsonify({"message": "Incomplete entry"}), 401)
    user = [user for user in User.users if user.username == username]
    if user:
        if password == user[0].password:
            session['logged_in'] = True
            session['username'] = username
            return make_response(jsonify({"message": "Login Successful"}), 200)

        else:
            return make_response(jsonify({"message": "Wrong Password"}), 409)

    else:
        return make_response(jsonify({"message": "Wrong username"}), 409)

# reset password
@app.route('/api/v1/auth/reset_password', methods = ['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    newpassword = data.get('newpassword')
    if email is None:
        return make_response(jsonify({"message": "Missing key"}), 409)
    if type(newpassword) != str:
        return make_response(jsonify({"message": "Wrong format"}), 409)
    user = [user for user in User.users if user.email == email]
    if user:
        try:
            user[0].reset_password(newpassword)
        except AssertionError as err:
            return make_response(jsonify({"error": err.args[0]}), 409)
        return make_response(jsonify({"message": "Reset Successful"}), 201)
    else:
        return make_response(jsonify({"message": "User with that email does not exist"}), 404)

# check  if user is logged in


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return make_response(jsonify({"Unauthorised": "Please login first"}), 401)
    return wrap

# Change password


@app.route('/api/v1/auth/change-password', methods=['POST'])
@is_logged_in
def change_password():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    newpassword = data.get('newpassword')
    user = [x for x in User.users if x.username == username]
    if user and password != user[0].password:
        return make_response(jsonify({"message": "Enter your Current Password"}), 409)
    elif newpassword == user[0].password:
        return make_response(jsonify({"message": "Use a Different New Password"}), 409)

    else:
        try:
            user[0].reset_password(newpassword)
        except AssertionError as err:
            return make_response(jsonify({"error": err.args[0]}), 409)
    return make_response(jsonify({"message": "Reset Successful"}), 201)

# Logout User


@app.route('/api/v1/auth/logout', methods=['POST'])
@is_logged_in
def logout():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # check if the user details exist in the list, otherwise deny access.
    user = [user for user in User.users if user.username == username]
    if user:
        if password == user[0].password:
            session.clear()
            return make_response(jsonify({"message": "Logout Successful"}), 200)

        else:
            return make_response(jsonify({"message": "Login First"}), 404)

    else:
        return make_response(jsonify({"message": "User not found, Login First"}), 404)


# Create new business
@app.route('/api/v1/auth/businesses', methods=['POST'])
@is_logged_in
def create_business():
    data = request.get_json()
    name = data.get("name")
    category = data.get("category")
    location = data.get("location")
    description = data.get("description")
    # check if the business details already in the list, otherwise create the object in the list
    available_names = [business.name for business in Business.businesses]
    if name in available_names:
        return make_response(jsonify({"error": "Business already Exist, use another name"}), 409)

    else:
        try:
            business = Business.register_business(
                name, category, location, description)
        except AssertionError as err:
            return make_response(jsonify({"error": err.args[0]}), 409)
        myresponse = {'name': business.name, 'category': business.category,
                      'location': business.location, 'description': business.description}
    return make_response(jsonify(myresponse), 201)

# Get all the businesses


@app.route('/api/v1/auth/businesses', methods=['GET'])
@is_logged_in
def view_businesses():
    mybusinesses = [{business.id: [business.name, business.category, business.location]
                     for business in Business.businesses}]
    if mybusinesses == [{}]:
        return make_response(jsonify({"businesses": "No Business Entry"}), 404)
    else:
        return make_response(jsonify({"businesses": mybusinesses}), 200)

# Get a business by id


@app.route('/api/v1/auth/business/<int:id>/', methods=['GET'])
@is_logged_in
def get_business(id):
    mybusiness = [business for business in Business.businesses if business.id == id]
    if mybusiness:
        mybusiness = mybusiness[0]
        return make_response(jsonify({"business": {'name': mybusiness.name,
        'category': mybusiness.category, 'location': mybusiness.location, 
        'description': mybusiness.description}}), 200)
    else:
        return make_response(jsonify({"message": "Business not available", }), 404)

# Update business


@app.route('/api/v1/auth/business/<int:id>', methods=['PUT'])
@is_logged_in
def update_business(id):
    data = request.get_json()
    newname = data.get("name")
    newcategory = data.get("category")
    newlocation = data.get("location")
    newdescription = data.get("description")
    mybusiness = [business for business in Business.businesses if business.id == id]
    if mybusiness:
        available_names = [business.name for business in Business.businesses]
        if newname in available_names: 
            return make_response(jsonify({"error": "Business already Exist, use another name"}), 409)
        try:
            mybusiness[0].update_business(
            newname, newcategory, newlocation, newdescription)
        except AssertionError as err:
            return make_response(jsonify({"error": err.args[0]}), 409)
        return make_response(jsonify({"message": "Business Updated", }), 201)
    else:
        return make_response(jsonify({"message": "Business not available", }), 404)

# Delete business


@app.route('/api/v1/auth/business/<int:id>/', methods=['DELETE'])
@is_logged_in
def delete_business(id):
    mybusiness = [business for business in Business.businesses if business.id == id]
    if mybusiness:
        mybusiness = mybusiness[0]
        Business.businesses.remove(mybusiness)
        return make_response(jsonify({"message": "Business deleted", }), 200)
    else:
        return make_response(jsonify({"message": "No such Business", }), 404)

# Add a review for a business


@app.route('/api/v1/auth/<int:businessid>/reviews', methods=['POST'])
@is_logged_in
def reviews(businessid):
    data = request.get_json()
    reviewbody = data.get("description")

    if reviewbody.strip() == "":
        return make_response(jsonify({"error": "Empty review not allowed"}))

    if len(reviewbody) < 5:
        return make_response(jsonify({"error": "Review too short"}))

    mybusiness = [
        business for business in Business.businesses if business.id == businessid]
    if mybusiness:
        business_review = Review(reviewbody, businessid)
        business_reviews.append(business_review)
        return make_response(jsonify({"message": "Review added Successfully"}), 201)
    else:
        return make_response(jsonify({"message": "Business with that ID does not exist"}), 404)


# Get all reviews for a business
@app.route('/api/v1/auth/<int:businessid>/reviews', methods=['GET'])
@is_logged_in
def myreviews(businessid):
    myreviews = [review for review in business_reviews if review.businessid == businessid]

    review_info = {}
    for a_review in myreviews:
        review_info['businessid'] = a_review.businessid
        review_info['description'] = a_review.reviewbody
    if review_info == {}:
        return make_response(jsonify({"message": "No Reviews available"}), 404)
    else:
        return make_response(jsonify({"Reviews": review_info}), 200)
