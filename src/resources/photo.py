from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    # get_jwt_claims,
    # get_jwt_identity,
    # jwt_optional,
    # fresh_jwt_required,
)
from models.photo import PhotoModel

BLANK_ERROR = "'{}' cannot be blank."
NAME_ALREADY_EXISTS = "An photo with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the photo."
PHOTO_NOT_FOUND = "Photo not found."
PHOTO_DELETED = "Photo deleted."


class Photo(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help=BLANK_ERROR.format("price")
    )
    parser.add_argument(
        "label_id", type=int, required=True,
        help=BLANK_ERROR.format("label_id")
    )

    # Uncomment the @jwt decorators for using them only for logged in users

    # @jwt_required  # No longer needs brackets
    @classmethod
    def get(cls, name: str):
        photo = PhotoModel.find_by_name(name)
        if photo:
            return photo.json(), 200
        return {"message": "Photo not found."}, 404

    # @fresh_jwt_required
    @classmethod
    def post(cls, name: str):
        if PhotoModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400,

        data = Photo.parser.parse_args()

        photo = PhotoModel(name, **data)

        try:
            photo.save_to_db()
        except Exception:
            return {"message": ERROR_INSERTING}, 500

        return photo.json(), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str):
        # Uncomment the following for allowing only admins to delete
        # claims = get_jwt_claims()
        # if not claims["is_admin"]:
        #     return {"message": "Admin privilege required."}, 401

        photo = PhotoModel.find_by_name(name)
        if photo:
            photo.delete_from_db()
            return {"message": PHOTO_DELETED}, 200
        return {"message": PHOTO_NOT_FOUND}, 404

    @classmethod
    def put(cls, name: str):
        data = Photo.parser.parse_args()

        photo = PhotoModel.find_by_name(name)

        if photo:
            photo.price = data["price"]
        else:
            photo = PhotoModel(name, **data)

        photo.save_to_db()

        return photo.json(), 200


class PhotoList(Resource):
    # @jwt_optional
    @classmethod
    def get(cls):
        """
        Here we get the JWT identity, and then if the user is logged in
        (we were able to get an identity) we return the entire photo list.

        Otherwise we just return the photo names.

        This could be done with e.g. see orders that have been placed,
        but not see details about the orders unless the user has logged in.
        """
        # user_id = get_jwt_identity()
        photos = [photo.json() for photo in PhotoModel.find_all()]
        # if user_id:
        return {"photos": photos}, 200
        # return (
        #     {
        #         "photos": [photo["name"] for photo in photos],
        #         "message": "More data available if you log in.",
        #     },
        #     200,
        # )
