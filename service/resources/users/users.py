from flask import abort
from flask_restful import (Resource, reqparse,
                           fields, marshal_with)
from service.models import UserModel
from service import db

# Used for validateion
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, help="Please enter a name")
user_args.add_argument('email', type=str, help="Please enter an Email")

# Used for serialization
userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

class UsersGet(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users

class UserPost(Resource):
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201


class UserGet(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user: 
            abort(400, "User not found")
        return user, 200

class UserPatch(Resource):
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user: 
            abort(400, "User not found")
        user.name = args["name"]
        user.name = args["email"]
        db.session.commit()
        return user, 200

class UserDelete(Resource):
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user: 
            abort(400, "User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 204
