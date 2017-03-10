import json
import requests
from pprint import pprint

class Mytrello(object):
    __module__ = 'trello'
    def __init__(self, apikey, token=None):
        self._apikey = apikey
        self._token = token

    def search(self, board_id, query, modelTypes="all"):
        resp = requests.get("https://trello.com/1/search" % (),
                            params=dict(key=self._apikey, token=self._token,
                                        query=("%s" % (query)), idBoards=board_id, modelTypes=modelTypes))
        resp.raise_for_status()
        return json.loads(resp.content)

    def create_label(self, label_name, color, board_id):
        resp = requests.post("https://trello.com/1/labels/" % (),
                             params=dict(key=self._apikey, token=self._token),
                             data=dict(name=label_name, color=color, idBoard=board_id))
        resp.raise_for_status()
        return json.loads(resp.content)

    def assign_label_to_card(self, card_id, label_id):
        resp = requests.post("https://trello.com/1/cards/%s/idLabels/" % (card_id),
                             params=dict(key=self._apikey, token=self._token),
                             data=dict(value=label_id))
        resp.raise_for_status()
        return json.loads(resp.content)
