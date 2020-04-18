from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_secret_key'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

shelves = []


class Shelve(Resource):
    @jwt_required()
    def get(self, title):
        # shelve = next(filter(lambda x: x['title'] == title, shelves), None)
        # return {'shelve': None}, 200 if shelve else 404

        for shelve in shelves:
            if shelve['title'] == title:
                return shelve
        return {'shelve': None}, 404

    def post(self, title):
        # data = request.get_json()
        shelve = {'title': title, 'labels': []}
        shelves.append(shelve)
        return shelve, 201

    def delete(self, title):
        global shelves
        shelves = list(filter(lambda x: x['title'] != title, shelves))
        return {'message': 'Item deleted'}

    def put(self, title):
        # Only labels argument is accepted for update
        # this can be added in the class itself
        parser = reqparse.RequestParser()
        parser.add_argument(
            'labels',
            type=float,
            required=True,
            help="This field cannot be left blank!"
        )
        data = parser.parse_args()
        shelve = next(filter(lambda x: x['title'] == title, shelves), None)
        if shelve is None:
            shelve = {'title': title, 'labels': []}
            shelves.append(shelve)
        else:
            shelve.update(data)
        return shelve


class ShelveList(Resource):
    def get(self):
        return {'shelves': shelves}


api.add_resource(Shelve, '/shelve/<string:title>')
api.add_resource(ShelveList, '/shelves')

app.run(port=5000, debug=True)
