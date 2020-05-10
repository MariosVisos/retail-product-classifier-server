from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from flask_mail import Message
from passlib.hash import pbkdf2_sha256
from models.user import UserModel
from blacklist import BLACKLIST

BLANK_ERROR = "'{}' cannot be blank."
USER_ALREADY_EXISTS = "A user with that username already exists."
CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={user_id}> successfully logged out."
EMAIL_SENT_SUCCESSFULLY = "Email sent successfully"

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "username", type=str, required=True, help=BLANK_ERROR.format("username")
)
_user_parser.add_argument(
    "password", type=str, required=False, help=BLANK_ERROR.format("password")
)


class UserRegister(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return (
                {
                    "message": USER_ALREADY_EXISTS,
                    "reason": "user_already_exists"
                },
                400
            )

        username = data["username"]
        password = pbkdf2_sha256.hash(data["password"])
        user = UserModel(username, password)
        user.save_to_db()

        return {"message": CREATED_SUCCESSFULLY, "user": user.json()}, 201


class User(Resource):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when
    we are manipulating data regarding the users.
    """

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        return user.json(), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        user.delete_from_db()
        return {"message": USER_DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data["username"])

        # this is what the `authenticate()` function did in security.py
        if user and pbkdf2_sha256.verify(data["password"], user.password):
            # identity= is what the identity() function
            #  did in security.py—now stored in the JWT
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return (
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user.json()},
                200
            )

        return (
            {"message": INVALID_CREDENTIALS, "reason": "invalid_credentials"},
            401
        )


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        # jti is "JWT ID", a unique identifier for a JWT.
        jti = get_raw_jwt()["jti"]
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


class ResetPassword(Resource):
    def __init__(self, **kwargs):
        # smart_engine is a black box dependency
        self.mail = kwargs['mail']

    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data["username"])

        if user:
            msg = Message("Hello",
                          recipients=["mariakos7@hotmail.com"],
                          body="This is a test email with Gmail and Python!")
            self.mail.send(msg)
            return {"message": EMAIL_SENT_SUCCESSFULLY}, 200

        return {"message": USER_NOT_FOUND}, 404
