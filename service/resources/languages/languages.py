from flask import abort
from flask_restful import Resource
from service.utils.languages import getLanguages



class LanguagesGet(Resource):
    def map_languages(self, data):
        lang_data = []
        for lang in data:
            lang_pair = {
                    'lang_code': lang[0],
                    'lang_label': lang[1]
                }
            lang_data.append(lang_pair)
        return lang_data

    def get(self):
        languages = self.map_languages(getLanguages())
        return languages


class LanguageGet(Resource):
    def get(self, lang_code):
        lang_pair = [entry for entry in getLanguages() if entry[0] == lang_code]
        if not lang_pair: 
            abort(400, "Language not supported")
        return {
            'lang_code': lang_pair[0],
            'lang_label': lang_pair[1]
        }, 200
