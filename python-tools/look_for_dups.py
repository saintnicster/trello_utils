from trello import TrelloClient
from trello import Label as TrelloLabel
from pprint import pprint
from inspect import getmembers
from issow_trello_setup import *

backlog_board = ISSOW_TRELLO_CLIENT.get_board(TRELLO_IDS.BOARDS.BACKLOG)
inwork_board = ISSOW_TRELLO_CLIENT.get_board(TRELLO_IDS.BOARDS.INWORK)

all_cards = inwork_board.all_cards( ) + backlog_board.all_cards( ) 

sorted_cards = {}

for card in all_cards:
    incident_number = card.name.partition('-')[0].strip()
    if incident_number not in sorted_cards:
        sorted_cards[incident_number] = []
    
    sorted_cards[incident_number].append(card)

for incident, possible_dupe in sorted_cards.items():
    length = len(possible_dupe)
    if length > 1:
        print("%s Duplicate cards found for incident %s" % (length, incident) )
