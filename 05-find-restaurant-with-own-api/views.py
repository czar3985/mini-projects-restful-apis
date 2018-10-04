from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)




foursquare_client_id = 'BG0BB2V1COPP0FG1BJFGIPT14KAGKTYE4FPKFHIBRKVLDIST'

foursquare_client_secret = 'PJI0EARPCYSZ32NP5RGYZ3BWKO3R5LGB2CW30BV2QJMKVXIJ'

google_api_key = 'AIzaSyBBphfo58u3NkrgCv9wQXXwwyUpVIXYCF4'

engine = create_engine('sqlite:///restaurants.db',
                       connect_args={'check_same_thread': False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


def getAllRestaurants():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[restaurant.serialize
                                for restaurant in restaurants])


def makeANewRestaurant(location, mealType):
    restaurantInfo = findARestaurant(mealType, location)
    if restaurantInfo == "No Restaurants Found":
        return "No Restaurants Found"

    newRestaurant = Restaurant(restaurant_name=restaurantInfo['name'],
                               restaurant_address=restaurantInfo['address'],
                               restaurant_image=restaurantInfo['image'])
    session.add(newRestaurant)
    session.commit()

    newRestaurant = session.query(Restaurant).filter_by(
        restaurant_name=restaurantInfo['name']).first()
    return jsonify(Restaurant=[newRestaurant.serialize])


def getRestaurant(id):
    restaurant = session.query(Restaurant).filter_by(id=id).first()
    return jsonify(Restaurant=[restaurant.serialize])


def updateRestaurant(id, name, location, image):
    # TODO: session query at the handler function
    restaurant = session.query(Restaurant).filter_by(id=id).first()
    # Only perform update if address, name, image is available. see solution code
    restaurant.restaurant_name = name
    restaurant.restaurant_address = location
    restaurant.restaurant_image = image
    session.add(restaurant)
    session.commit()
    return jsonify(Restaurant=[restaurant.serialize])


def deleteRestaurant(id):
    restaurant = session.query(Restaurant).filter_by(id=id).first()
    session.delete(restaurant)
    session.commit()
    #error messages in jsonify
    return "Restaurant was deleted"


@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
    if request.method == 'GET':
        return getAllRestaurants()
    elif request.method == 'POST':
        location = request.args.get('location', '')
        mealType = request.args.get('mealType', '')
        return makeANewRestaurant(location, mealType)


@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
    if request.method == 'GET':
        return getRestaurant(id)

    elif request.method == 'PUT':
        name = request.args.get('name', '')
        location = request.args.get('address', '')
        image = request.args.get('image', '')
        return updateRestaurant(id, name, location, image)

    elif request.method == 'DELETE':
        return deleteRestaurant(id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)



