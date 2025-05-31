from flask_restful import (Resource)


class Home(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'AGPB service'
        }, 200
