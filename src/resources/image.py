from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    # get_jwt_claims,
    # get_jwt_identity,
    # jwt_optional,
    fresh_jwt_required,
)
from models.image import ImageModel


class Image(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "label_id", type=int, required=True, help="Every image needs a label_id."
    )

    # Uncomment the @jwt decorators for using them only for logged in users

    # @jwt_required  # No longer needs brackets
    def get(self, name):
        image = ImageModel.find_by_name(name)
        if image:
            return image.json(), 200
        return {"message": "Image not found."}, 404

    # @fresh_jwt_required
    def post(self, name):
        if ImageModel.find_by_name(name):
            return (
                {"message": "An image with name '{}' already exists.".format(
                    name)},
                400,
            )

        data = Image.parser.parse_args()

        image = ImageModel(name, **data)

        try:
            image.save_to_db()
        except:
            return {"message": "An error occurred while inserting the image."}, 500

        return image.json(), 201

    @jwt_required
    def delete(self, name):
        # Uncomment the following for allowing only admins to delete
        # claims = get_jwt_claims()
        # if not claims["is_admin"]:
        #     return {"message": "Admin privilege required."}, 401

        image = ImageModel.find_by_name(name)
        if image:
            image.delete_from_db()
            return {"message": "Image deleted."}, 200
        return {"message": "Image not found."}, 404

    def put(self, name):
        data = Image.parser.parse_args()

        image = ImageModel.find_by_name(name)

        if image:
            image.price = data["price"]
        else:
            image = ImageModel(name, **data)

        image.save_to_db()

        return image.json(), 200


class ImageList(Resource):
    # @jwt_optional
    def get(self):
        """
        Here we get the JWT identity, and then if the user is logged in (we were able to get an identity)
        we return the entire image list.

        Otherwise we just return the image names.

        This could be done with e.g. see orders that have been placed, but not see details about the orders
        unless the user has logged in.
        """
        # user_id = get_jwt_identity()
        images = [image.json() for image in ImageModel.find_all()]
        # if user_id:
        return {"images": images}, 200
        # return (
        #     {
        #         "images": [image["name"] for image in images],
        #         "message": "More data available if you log in.",
        #     },
        #     200,
        # )
