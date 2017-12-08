from trello import TrelloClient
from trello import Label as TrelloLabel
from pprint import pprint
from inspect import getmembers

TRELLO_IDS = type('trello_ids', 
    (object,), {
        "BOARDS" : type('board_ids',(object,), { "BACKLOG" : '587d4739aacd90eb33fedfce', "INWORK" : '59b801ead00a15fd62d1fe05' } ),
        "LISTS"  : type('list_ids' ,(object,), { "NEWLY_CREATED" : '587e244b50ed39d516edf94f', "NOT_BVILLE" : '598b14d18ce45e0e70ace903', "RESOLVED" : '587fb500aa3ee04f092ccc7d'} ),
        "LABELS" : type('label_ids',(object,), { "BU_PRIORITY" : '58823fceced82109ffdda066',"CONFIG" : '58a46d1eced82109ff4b1165' } )
        }
    )

client = TrelloClient(
    api_key='***REMOVED***',
    api_secret='***REMOVED***',
    token='***REMOVED***',
    token_secret='***REMOVED***'
)

backlog_board = client.get_board(TRELLO_IDS.BOARDS.BACKLOG)
inwork_board = client.get_board(TRELLO_IDS.BOARDS.INWORK)

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
