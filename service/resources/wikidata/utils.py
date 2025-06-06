
import requests
import json
from flask import make_response
from common import base_url
from difflib import get_close_matches

def make_api_request(url, PARAMS):
    """ Makes request to an end point to get data

        Parameters:
            url (str): The Api url end point
            PARAMS (obj): The parameters to be used as arguments

        Returns:
            data (obj): Json object of the recieved data.
    """

    try:
        S = requests.Session()
        r = S.get(url=url, params=PARAMS)
        data = r.json()
    except Exception as e:
        return {
            'message': str(e),
            'status_code': 503
        }

    if data is None:
        return None
    else:
        return data


def process_search_results(search_results, search, src_lang, ismatch_search):
    """
    """
    src_match = {'type': 'label', 'language': src_lang, 'text': search}
    lexeme_result = []
    if ismatch_search:
        for result in search_results:
            res_item = {}
            if result['match'] == src_match:
                res_item['id'] = result['id']
                res_item['label'] = result['label']
                res_item['language'] = src_lang
                res_item['description'] = result['description']
                lexeme_result.append(res_item) 
    else:
        for res in search_results:
            res_item = {}
            res_item['id'] = res['id']
            res_item['label'] = res['label']
            res_item['language'] = src_lang
            res_item['description'] = res['description']
            lexeme_result.append(res_item)

    return lexeme_result


def lexemes_search(search, src_lang, ismatch):
    """
    """
    PARAMS = {
        "action": "wbsearchentities",
        "format": "json",
        "language": src_lang,
        "type": "lexeme",
        "uselang": src_lang,
        "search": search,
        "limit": 15
    }

    wd_search_results = make_api_request(base_url, PARAMS)

    if 'status_code' in list(wd_search_results.keys()):
        return wd_search_results

    search_result_data = process_search_results(wd_search_results['search'],
                                                search, src_lang, bool(ismatch))

    return search_result_data


def process_lexeme_sense_data(senses_data, lang_1, lang_2):
    """
    """
    processed_data = {}

    for sense in senses_data['senses']:
        sense_base = {}
        sense_base['id'] = sense['id']
        sense_gloss = sense['glosses']
        if sense_gloss:
            for lang in [lang_1, lang_2]:
                if lang in sense_gloss:
                    processed_data.setdefault(sense['id'], [])
                    processed_data[sense['id']].append(sense_gloss[lang])

    return [processed_data]


def get_lexeme_sense_glosses(lexeme_id, src_lang, lang_1, lang_2):
    """ 
    Gloses for a particular lexeme
    """
    PARAMS = {
        "action": "wbgetentities",
        "format": "json",
        "languages": src_lang,
        "ids": lexeme_id
    }

    lexeme_senses_data = make_api_request(base_url, PARAMS)

    if 'status_code' in list(lexeme_senses_data.keys()):
        return lexeme_senses_data

    glosses_data = process_lexeme_sense_data(lexeme_senses_data['entities'][lexeme_id],
                                            lang_1, lang_2)
    return glosses_data


def process_lexeme_form_data(search_term, data, lang_1, lang_2):
    processed_data = {}
    print('data ', data)

    for form in data:
        for lang in [lang_1, lang_2]:
            reps_match = {lang: {'language': lang, 'value': search_term}}

            if form['representations'] == reps_match and form['claims']:
                processed_data.setdefault(form['id'], [])
                form_claims_audios = form['claims']['P443']

                potential_match_audio = []
                for audio_claim in form_claims_audios:
                    # TODO: Find a way to best match serach term to audio
                    potential_match_audio.append(audio_claim['mainsnak']['datavalue']['value'])

                best_match_audio = get_close_matches(lang + '-' + search_term, potential_match_audio)
                processed_data[form['id']].append({
                    'language': lang,
                    'audio': best_match_audio[0] if len(best_match_audio ) > 1 else best_match_audio
                })
    return [processed_data]


def get_lexeme_forms_audio(search_term, lexeme_id, src_lang, lang_1, lang_2):
    PARAMS = {
        "action": "wbgetentities",
        "format": "json",
        "languages": src_lang,
        "ids": lexeme_id
    }

    lexeme_data = make_api_request(base_url, PARAMS)

    if not lexeme_data:
        return 'Failure'

    form_data = process_lexeme_form_data(search_term, lexeme_data['entities'][lexeme_id]['forms'],lang_1, lang_2)
    return form_data
