from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    # get_jwt_claims,
    # get_jwt_identity,
    # jwt_optional,
    fresh_jwt_required,
)
from models.label import LabelModel

BLANK_ERROR = "'{}' cannot be blank."
NAME_ALREADY_EXISTS = "A label with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the label."
LABEL_NOT_FOUND = "Label not found."
LABEL_DELETED = "Label deleted."


class Label(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help=BLANK_ERROR.format("price")
    )
    parser.add_argument(
        "dataset_id", type=int, required=True, help=BLANK_ERROR.format("dataset_id")
    )

    # Uncomment the @jwt decorators for using them only for logged in users

    # @jwt_required  # No longer needs brackets
    @classmethod
    def get(cls, name: str):
        label = LabelModel.find_by_name(name)
        if label:
            return label.json(), 200
        return {"message": LABEL_NOT_FOUND}, 404

    # @fresh_jwt_required
    @classmethod
    def post(cls, name: str):
        if LabelModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400,

        data = Label.parser.parse_args()

        label = LabelModel(name, **data)

        try:
            label.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return label.json(), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str):
        # Uncomment the following for allowing only admins to delete
        # claims = get_jwt_claims()
        # if not claims["is_admin"]:
        #     return {"message": "Admin privilege required."}, 401

        label = LabelModel.find_by_name(name)
        if label:
            label.delete_from_db()
            return {"message": LABEL_DELETED}, 200
        return {"message": LABEL_NOT_FOUND}, 404

    @classmethod
    def put(cls, name: str):
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
    @classmethod
    def get(cls):
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
