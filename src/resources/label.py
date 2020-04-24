from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    # get_jwt_claims,
    # get_jwt_identity,
    # jwt_optional,
    fresh_jwt_required,
)
from models.label import LabelModel


class Label(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "dataset_id", type=int, required=True, help="Every label needs a dataset_id."
    )

    # Uncomment the @jwt decorators for using them only for logged in users

    # @jwt_required  # No longer needs brackets
    def get(self, name: str):
        label = LabelModel.find_by_name(name)
        if label:
            return label.json(), 200
        return {"message": "Label not found."}, 404

    # @fresh_jwt_required
    def post(self, name: str):
        if LabelModel.find_by_name(name):
            return (
                {"message": "An label with name '{}' already exists.".format(
                    name)},
                400,
            )

        data = Label.parser.parse_args()

        label = LabelModel(name, **data)

        try:
            label.save_to_db()
        except:
            return {"message": "An error occurred while inserting the label."}, 500

        return label.json(), 201

    @jwt_required
    def delete(self, name: str):
        # Uncomment the following for allowing only admins to delete
        # claims = get_jwt_claims()
        # if not claims["is_admin"]:
        #     return {"message": "Admin privilege required."}, 401

        label = LabelModel.find_by_name(name)
        if label:
            label.delete_from_db()
            return {"message": "Label deleted."}, 200
        return {"message": "Label not found."}, 404

    def put(self, name: str):
        data = Label.parser.parse_args()

        label = LabelModel.find_by_name(name)

        if label:
            label.price = data["price"]
        else:
            label = LabelModel(name, **data)

        label.save_to_db()

        return label.json(), 200


class LabelList(Resource):
    # @jwt_optional
    def get(self):
        """
        Here we get the JWT identity, and then if the user is logged in (we were able to get an identity)
        we return the entire label list.

        Otherwise we just return the label names.

        This could be done with e.g. see orders that have been placed, but not see details about the orders
        unless the user has logged in.
        """
        # user_id = get_jwt_identity()
        labels = [label.json() for label in LabelModel.find_all()]
        # if user_id:
        return {"labels": labels}, 200
        # return (
        #     {
        #         "labels": [label["name"] for label in labels],
        #         "message": "More data available if you log in.",
        #     },
        #     200,
        # )
