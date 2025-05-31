import os
from flask import redirect
from service import app, api, prefix
from service.home.home import Home
from swagger.swaggerConfig import SwaggerConfig
from service.resources.users.users import UsersGet, UserPost, UserGet, UserPatch, UserDelete


api.add_resource(SwaggerConfig, '/swagger-config')

api.add_resource(UsersGet, '/users/')
api.add_resource(UserPost, '/users/')
api.add_resource(UserGet, '/users/<int:id>')
api.add_resource(UserPatch, '/users/<int:id>')
api.add_resource(UserDelete, '/users/<int:id>')
api.add_resource(Home, '/home')


@app.route('/')
def redirect_to_prefix():
    print('redirecting to prefix')
    if prefix != '':
        return redirect(prefix)


if __name__ == '__main__':
    app.run(debug=True)
