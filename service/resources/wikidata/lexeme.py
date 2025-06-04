from flask import abort
from flask_restful import (Resource, reqparse,
                           fields, marshal_with)

from .utils import lexemes_search, get_lexeme_sense_glosses, get_lexeme_forms_audio


# Used for validateion
lexeme_args = reqparse.RequestParser()
form_audio_args = reqparse.RequestParser()

lexeme_args.add_argument('search', type=str, help="Please provide a search term")
lexeme_args.add_argument('src_lang', type=str, help="Source language is required")
lexeme_args.add_argument('id', type=str, help="Lexeme ID is required")
lexeme_args.add_argument('property', type=str, help="Please provide a property to fetch")
lexeme_args.add_argument('lang_1', type=str, help="Please provide the first language")
lexeme_args.add_argument('lang_2', type=str, help="Please provide the second language")
lexeme_args.add_argument('ismatch', type=str, help="Match lexeme in language")

form_audio_args.add_argument('search_term', type=str, help="Please provide a search term")
form_audio_args.add_argument('id', type=str, help="Lexeme ID is required")
form_audio_args.add_argument('src_lang', type=str, help="Source language is required")
form_audio_args.add_argument('lang_1', type=str, help="Please provide the first language")
form_audio_args.add_argument('lang_2', type=str, help="Please provide the second language")


# Used for serialization
lexemeSearcFields = {
    'id': fields.String,
    'label': fields.String,
    'language': fields.String,
    'description': fields.String,
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
        if not id or not args['lang_1'] or not args['lang_2'] or not args['src_lang']:
            abort(400, f'Please provide required parameters {str(list(args.keys()))}')

        lexeme_glosses = get_lexeme_sense_glosses(args['id'], args['src_lang'], args['lang_1'], args['lang_2'])
        return lexeme_glosses, 200


class LexemeFormAudioGet(Resource):
    def post(self, id):
        args = form_audio_args.parse_args()
        if not args['search_term'] or not args['lang_1'] or not args['lang_2'] or not args['id'] \
            or not args['src_lang']:
            abort(400, f'Please check required parameters {str(list(args.keys()))}')
        lexeme_audios = get_lexeme_forms_audio(args['search_term'], args['id'], args['src_lang'],
                                               args['lang_1'], args['lang_2'])
        return lexeme_audios


# Todo: Get Lexeme Form Which matches lang1 and 2
        # Check if they have P443
            # - For every match form, get its claims with P443
            # - Return Values if present or empty if not
        # HINT: similar to LexemeGlossesGet logic
