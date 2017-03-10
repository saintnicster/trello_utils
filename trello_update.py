
import csv
import json
import requests
from trello import TrelloApi
from pprint import pprint
from inspect import getmembers
from Mytrello import Mytrello

TRELLO_APP_KEY = "***REMOVED***"
TOKEN = "***REMOVED***"
ISSOW_BOARD_ID = '587d4739aacd90eb33fedfce'

def get_xref():
    in_dict = None
    with open('C:\\Users\\fajarn\\Documents\\backlog_importer\\trello-servicenow-xref.json', 'r') as xref_infile:
        in_dict = json.load(xref_infile)

    return in_dict

def read_servicenow_file():
    file_rows = []
    with open('C:\\Users\\fajarn\\Documents\\backlog_importer\\incident.csv') as csv_file:
        file_reader = csv.DictReader(csv_file)
        for row in file_reader:
            file_rows.append(row)
    return file_rows


def search_by_incident(incident_number):
    resp = requests.get("https://trello.com/1/search" % (),
                        params=dict(key=TRELLO_APP_KEY, token=TOKEN,
                                    query=("%s" % (incident_number)), idBoards=ISSOW_BOARD_ID, modelTypes="cards",
                                    card_fields="id"))
    resp.raise_for_status()
    card_id = json.loads(resp.content)
    try:
        card_id = card_id["cards"][0]['id']
    except KeyError :
        card_id = None
    return card_id

trello = TrelloApi(TRELLO_APP_KEY, TOKEN)
trello.extras = Mytrello(TRELLO_APP_KEY, TOKEN)

sn_trello_xref = get_xref()
new_sn_records = read_servicenow_file()
# issow_cards = trello.boards.get_card(ISSOW_BOARD_ID,None,None,None,None,None,None,"id,name,desc")
# for card in issow_cards:
#     trello_lookupcard["id"]

for incident in new_sn_records:
    if incident['number'] not in sn_trello_xref:
        result = search_by_incident(incident['number'])
        if result == None:
            pprint("NEW RECORD! - %s" % incident['number'])
        sn_trello_xref[incident['number']] = result

    
    card_id = sn_trello_xref[incident['number']]

    createdon_timestamp = "S-Now Creation - %s\n\n" % (incident['sys_created_on'])
    
    if (incident['description'].startswith(createdon_timestamp) == False):
        incident['description'] = createdon_timestamp + incident['description']
    print(incident['description'])
    break
    #trello.cards.update_desc(card_id,incident['description'])

# results = trello.extras.search(ISSOW_BOARD_ID, "INC2429622", "cards")
# results['cards'][0]['id']
