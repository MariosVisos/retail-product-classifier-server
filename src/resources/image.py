from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import send_file, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback
import os

from libs import image_helper
from schemas.image import ImageSchema
from models.image import ImageModel
from models.label import LabelModel


image_schema = ImageSchema()

IMAGE_UPLOADED = "Image '{}' uploaded"
IMAGE_ILLEGAL_EXTENSION = "The extension '{}' is not allowed"
IMAGE_ILLEGAL_FILENAME = "The filename '{}' is not allowed"
IMAGE_NOT_FOUND = "The IMAGE '{}' is not found"
IMAGE_DELETED = "The IMAGE '{}' is deleted"
IMAGE_DELETE_FAILED = "Failed deleting the image"
ERROR_INSERTING = "An error occurred while inserting the photo."


class ImageUpload(Resource):
    # @jwt_required
    def post(self):
        """
        This endpoint is used to upload an image file. It uses the
        JWT to retrieve user information and save the image in the
        user's folder. If a file with the same name exists in the
        user's folder, name conflicts will be automatically
        resolved by appending a underscore and a smallest
        unused integer. (eg. filename.png to filename_1.png).
        """
        data = image_schema.load(request.files)
        label_id = request.form.get("label_id")
        print("upload_image -> label_id: ", label_id)
        label = LabelModel.find_by_id(label_id)
        print("label: ", label)
        # user_id = get_jwt_identity()
        folder = label.name  # static/images/{label.name}
        try:
            # save(self, storage, folder=None, name=None)
            image_path = image_helper.save_image(data["image"], folder=folder)
            # here we only return the basename of the image and hide the
            # internal folder structure from our user
            basename = image_helper.get_basename(image_path)

            # create image in db
            image = ImageModel(basename, label.id)
            try:
                image.save_to_db()
            except Exception:
                return {"message": ERROR_INSERTING}, 500

            return {"message": IMAGE_UPLOADED.format(image.name)}, 201
        except UploadNotAllowed:  # forbidden file type
            extension = image_helper.get_extension(data["image"])
            return {"message": IMAGE_ILLEGAL_EXTENSION.format(extension)}, 400


class Image(Resource):
    # @ jwt_required
    def get(self, filename: str):
        """
        This endpoint returns the requested image if exists. It will use
        JWT to retrieve user information and look for the image
        inside the user's folder.
        """
        # user_id = get_jwt_identity()
        # folder = f"user_{user_id}"
        folder = "Kellogg's Special K"
        # check if filename is URL secure
        if not image_helper.is_filename_safe(filename):
            return {"message": IMAGE_ILLEGAL_FILENAME.format(filename)}, 400
        try:
            # try to send the requested file to the user with status code 200
            print("debug get path", image_helper.get_path(
                filename, folder=folder))
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            return {"message": IMAGE_NOT_FOUND.format(filename)}, 404

    @ jwt_required
    def delete(self, filename: str):
        """
        This endpoint is used to delete the requested image under the user's
        folder. It uses the JWT to retrieve user information.
        """
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        # check if filename is URL secure
        if not image_helper.is_filename_safe(filename):
            return {"message": IMAGE_ILLEGAL_FILENAME.format(filename)}, 400

        try:
            os.remove(image_helper.get_path(filename, folder=folder))
            return {"message": IMAGE_DELETED.format(filename)}, 200
        except FileNotFoundError:
            return {"message": IMAGE_NOT_FOUND.format(filename)}, 404
        except Exception:
            traceback.print_exc()
            return {"message": IMAGE_DELETE_FAILED}, 500


class ImageList(Resource):
    # @jwt_optional
    @classmethod
    def get(cls):
        """
        Here we get the JWT identity, and then if the user is logged in
        (we were able to get an identity) we return the entire label list.

        Otherwise we just return the label names.

        This could be done with e.g. see orders that have been placed,
        but not see details about the orders unless the user has logged in.
        """
        # user_id = get_jwt_identity()
        data = parser.parse_args()
        label_id = data['label_id']
        labels = None
        if label_id:
            images = [image.json()
                      for image in ImageModel.find_by_label_id(label_id)]
        else:
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


# class AvatarUpload(Resource):
#     @jwt_required
#     def put(self):
#         """
#         This endpoint is used to upload user avatar. All avatars are named
#         after the user's id in such format: user_{id}.{ext}.
#         It will overwrite the existing avatar.
#         """
#         data = image_schema.load(request.files)
#         filename = f"user_{get_jwt_identity()}"
#         folder = "avatars"
#         avatar_path = image_helper.find_image_any_format(filename, folder)
#         if avatar_path:
#             try:
#                 os.remove(avatar_path)
#             except:
#                 return {"message": gettext("avatar_delete_failed")}, 500

#         try:
#             ext = image_helper.get_extension(data["image"].filename)
#             avatar = filename + ext  # use our naming format + true extension
#             avatar_path = image_helper.save_image(
#                 data["image"], folder=folder, name=avatar
#             )
#             basename = image_helper.get_basename(avatar_path)
#             return (
#               {"message": gettext("avatar_uploaded").format(basename)}, 200
#             )
#         except UploadNotAllowed:  # forbidden file type
#             extension = image_helper.get_extension(data["image"])
#             return (
#            {"message": gettext("image_illegal_extension").format(extension)},
#               400
#             )


# class Avatar(Resource):
#     @classmethod
#     def get(cls, user_id: int):
#         """
#         This endpoint returns the avatar of the user specified by user_id.
#         """
#         folder = "avatars"
#         filename = f"user_{user_id}"
#         avatar = image_helper.find_image_any_format(filename, folder)
#         if avatar:
#             return send_file(avatar)
#         return {"message": gettext("avatar_not_found")}, 404
