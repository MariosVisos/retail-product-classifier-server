import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_uploads import configure_uploads, patch_request_class
from dotenv import load_dotenv
from flask_mail import Mail
# from flask_ngrok import run_with_ngrok


from db import db
from blacklist import BLACKLIST
from resources.user import (
    UserRegister, UserLogin, User, TokenRefresh, UserLogout, ResetPassword
)
from resources.label import Label, LabelList
from resources.dataset import Dataset, DatasetList
from resources.image import ImageUpload, Image
from libs.image_helper import IMAGE_SET

app = Flask(__name__, static_url_path='', static_folder='../static')

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD'],
    "MAIL_DEFAULT_SENDER": os.environ['EMAIL_USER']
}

app.config.update(mail_settings)
mail = Mail(app)

# run_with_ngrok(app)
load_dotenv(".env", verbose=True)
# load default configs from default_config.py
app.config.from_object("default_config")
# override with config.py (APPLICATION_SETTINGS points to config.py)
app.config.from_envvar("APPLICATION_SETTINGS")
# restrict max upload image size to 20MB
patch_request_class(app, 20 * 1024 * 1024)
configure_uploads(app, IMAGE_SET)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


# The following code can be used to add the is_admin flag to our app

# @jwt.user_claims_loader
# def add_claims_to_jwt(
#     identity
# ):  # Remember identity is what we define when creating the access token
#     if (
#         identity == 1
#     ):  # instead of hard-coding, we should read from a file or database
#           to get a list of admins instead
#         return {"is_admin": True}
#     return {"is_admin": False}


# This method will check if a token is blacklisted, and will be called
# automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return (
        decrypted_token["jti"] in BLACKLIST
    )  # Here we blacklist particular JWTs that have been created in the past.


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify(
        {"message": "The token has expired.", "error": "token_expired"}
    ), 401

# The following methods can be used to add jwt authorization to the app

# @jwt.invalid_token_loader
# def invalid_token_callback(
#     error
# ):  # we have to keep the argument here, since it's passed in by the caller
#       internally
#     return (
#         jsonify(
#             {"message": "Signature verification failed.", "error": "invalid
#              _token"}
#         ),
#         401,
#     )


# @jwt.unauthorized_loader
# def missing_token_callback(error):
#     return (
#         jsonify(
#             {
#                 "description": "Request does not contain an access token.",
#                 "error": "authorization_required",
#             }
#         ),
#         401,
#     )


# @jwt.needs_fresh_token_loader
# def token_not_fresh_callback():
#     return (
#         jsonify(
#             {"description": "The token is not fresh.",
#                 "error": "fresh_token_required"}
#         ),
#         401,
#     )


# @jwt.revoked_token_loader
# def revoked_token_callback():
#     return (
#         jsonify(
#             {"description": "The token has been revoked.", "error": "token
#              _revoked"}
#         ),
#         401,
#     )


api.add_resource(Dataset, "/dataset/<string:name>")
api.add_resource(DatasetList, "/datasets")
api.add_resource(Label, "/label/<string:name>")
api.add_resource(LabelList, "/labels")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(ResetPassword, "/reset_password",
                 resource_class_kwargs={'mail': mail})
api.add_resource(ImageUpload, "/upload/image")
api.add_resource(Image, "/image/<string:filename>")


if __name__ == "__main__":
    db.init_app(app)
    app.run(host='0.0.0.0')
