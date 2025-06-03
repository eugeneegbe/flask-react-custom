
import requests
from common import base_url

def make_api_request(url, PARAMS):
    """ Makes request to an end point to get data

        Parameters:
            url (str): The Api url end point
            PARAMS (obj): The parameters to be used as arguments

        Returns:
            data (obj): Json object of the recieved data.
    """

    S = requests.Session()
    r = S.get(url=url, params=PARAMS)
    data = r.json()

    if data is None:
        return {}
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
    search_result_data = process_search_results(wd_search_results['search'],
                                                search, src_lang, bool(ismatch))

    return search_result_data


def process_lexeme_sense_data(senses_data, lang_1, lang_2):
    """
    """
    processed_data = {}

    for sense in senses_data:
        sense_base = {}

        sense_base['id'] = sense['id']
        sense_gloss = sense['glosses']
        if sense_gloss:
            if lang_1 in list(sense_gloss.keys()):
                sense_base['language'] = lang_1 
                sense_base['value'] = sense_gloss[lang_1]['value']
                processed_data.setdefault(sense['id'], []).append(sense_base)
            if lang_2 in list(sense_gloss.keys()):
                print('sense_gloss 2 ', sense_gloss[lang_2])
                sense_base['language'] = lang_2
                sense_base['value'] = sense_gloss[lang_2]['value']
                processed_data.setdefault(sense['id'], []).append(sense_base)
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

    if not lexeme_senses_data:
        return 'Failure'

    glosses_data = process_lexeme_sense_data(lexeme_senses_data['entities'][lexeme_id]['senses'],
                                            lang_1, lang_2)
    return glosses_data
