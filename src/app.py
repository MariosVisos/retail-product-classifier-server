from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Shelve(Resource):
    def get(self, title):
        return {'shelve': title}


api.add_resource(Shelve, '/shelve/<string:title>')

app.run(port=5000)
