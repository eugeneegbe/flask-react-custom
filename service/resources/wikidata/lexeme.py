from flask import abort
from flask_restful import (Resource, reqparse,
                           fields, marshal_with)

from .utils import lexemes_search, get_lexeme_sense_glosses


# Used for validateion
lexeme_args = reqparse.RequestParser()
lexeme_args.add_argument('search', type=str, help="Please provide a search term")
lexeme_args.add_argument('src_lang', type=str, help="Source language is required")
lexeme_args.add_argument('id', type=str, help="Lexeme ID is required")
lexeme_args.add_argument('property', type=str, help="Please provide a property to fetch")
lexeme_args.add_argument('lang_1', type=str, help="Please provide the first language")
lexeme_args.add_argument('lang_2', type=str, help="Please provide the second language")
lexeme_args.add_argument('ismatch', type=str, help="Match lexeme in language")


# Used for serialization
lexemeSearcFields = {
    'id': fields.String,
    'label': fields.String,
    'language': fields.String,
    'description': fields.String,
}

lexemeGlossesFields = {
    'id': 
    [
        {
            'language': fields.String,
            'value': fields.String
        }
    ]
}


class LexemesGet(Resource):
    @marshal_with(lexemeSearcFields)
    def post(self):
        args = lexeme_args.parse_args()
        # TODO: Add arguments check
        if not args['search'] or not args['src_lang']:
            abort(400, f'Please provide required parameters {str(list(args.keys()))}')

        print('is00s0df0ds0f0sadfd match', args['ismatch'])

        lexemes = lexemes_search(args['search'], args['src_lang'], ismatch=int(args['ismatch']))
        return lexemes, 200


class LexemeGlossesGet(Resource):
    def post(self, id):
        args = lexeme_args.parse_args()
        # TODO: Add arguments check
        if not id or not args['lang_1'] or not args['lang_2'] or not args['src_lang']:
            abort(400, f'Please provide required parameters {str(list(args.keys()))}')

        lexeme_glosses = get_lexeme_sense_glosses(args['id'], args['src_lang'], args['lang_1'], args['lang_2'])
        print('lexeme_glosses', lexeme_glosses)
        return lexeme_glosses, 200

# Todo: Get Lexemes translations
