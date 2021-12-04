from flask_restful import Resource
from flask import request
from http import HTTPStatus
from models.recipe import User
from utils import check_password
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required
)


class TokenResource(Resource):
    """
    This class will implement the token resource,
    where the user is expected to login and gets the access token as response
    if the user is created
    """

    def post(self):
        """
        This method represents the post call with the body containing
        email and password
        :return: access_token in the response if the user is valid
        """
        json_data = request.get_json()

        email = json_data.get('email')
        password = json_data.get('password')

        user = User.get_by_email(email)
        if not user or not check_password(password, user.password):
            return {'message': 'username or password is incorrect'}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return {'access_token': access_token, 'refresh_token': refresh_token }, HTTPStatus.OK


class RefreshResource(Resource):
    """
    This class implements the refreshing the access token functionality
    """

    @jwt_required(refresh=True)
    def post(self):
        """
        This method will get the access token and creates the new access token using
        the refresh token and expired access
        :return:
        """
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': access_token}, HTTPStatus.OK