from ..wikidata.utils import make_api_request
from common import commons_url

def get_image_url(media_file):
    PARAMS = {
        "action": "query",
        "titles": "File:" + media_file,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    media_data = make_api_request(commons_url, PARAMS)
    image_id = list(media_data["query"]["pages"].keys())[0]
    if image_id and media_data["query"]["pages"][image_id]["imageinfo"]:
        return{
            'filename': media_file,
            'url': media_data["query"]["pages"][image_id]["imageinfo"][0]["url"]
        }
    else:
        return None
