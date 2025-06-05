from flask import abort
from flask_restful import (Resource, reqparse,
                           fields, marshal_with)

from .utils import get_image_url

# Used for validateion
media_args = reqparse.RequestParser()


media_args.add_argument('filename', type=str, help="Please provide a file name")



# Used for serialization
mediaFields = {
    'filename': fields.String,
    'url': fields.String
}

class CommonsFIleUrLPost(Resource):
    @marshal_with(mediaFields)
    def post(self, file_name):
        args = media_args.parse_args()
        # TODO: Add arguments check
        if not args['filename'] or not file_name:
            abort(400, f'Please provide required parameters {str(list(args.keys()))}')
        
        file_url = get_image_url(args['filename'])
        if not file_url:
            return {}

        return file_url, 200
