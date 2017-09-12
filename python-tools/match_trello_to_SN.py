from trello import TrelloClient
from pprint import pprint
from inspect import getmembers
from datetime import datetime
import json
import csv
from os import path

def read_servicenow_file():
    file_rows = []
    sn_dict = {}
    with open('C:\\Users\\fajarn\\Documents\\issow_trello_utils\\incident.csv') as csv_file:
        file_reader = csv.DictReader(csv_file)
        
        for row in file_reader:
            file_rows.append(row)
            sn_dict[row['number']] = row
    return { 'rows' : file_rows, 'dict' : sn_dict }

client = TrelloClient(
    api_key='***REMOVED***',
    api_secret='***REMOVED***',
    token='***REMOVED***',
    token_secret='***REMOVED***'
)
BACKLOG_BOARD_ID = '587d4739aacd90eb33fedfce'
INWORK_BOARD_ID = '59b801ead00a15fd62d1fe05'

CLOSED_LIST_ID = '587fb500aa3ee04f092ccc7d'

xref_dict = {}
list_lookup = {}

servicenow_dump = read_servicenow_file()

backlog_board = client.get_board(BACKLOG_BOARD_ID)
inwork_board = client.get_board(INWORK_BOARD_ID)

issow_lists = inwork_board.all_lists( ) + backlog_board.all_lists( )

for list in issow_lists:
    list_lookup[list.id] = list

#issow_cards = trello.boards.get_card(ISSOW_BOARD_ID,None,None,None,None,None,"all","idList,name,url,labels,closed")
all_cards = inwork_board.all_cards( ) + backlog_board.all_cards( ) 
for card in all_cards:
    incident_number = card.name.partition('-')[0].strip()
    xref_dict[incident_number] = card 

    if incident_number not in servicenow_dump['dict'] and card.idList != CLOSED_LIST_ID:
        print("%s missing in service now export - list %s" % (incident_number, list_lookup[card.idList].name))
        continue

    if card.closed == True:
        continue

    if card.idList == CLOSED_LIST_ID:
        if servicenow_dump['dict'][incident_number]['incident_state'] not in {'Resolved', 'Cancelled'}:
            print("%s closed in Trello, Status in SN = %s" % 
                (incident_number, servicenow_dump['dict'][incident_number]['incident_state']))
           
    

for record in servicenow_dump['rows']:
    if (record['number'] not in xref_dict):
        print("%s missing in trello" % (record['number']))
        continue
    list_id = xref_dict[record['number']].idList
    if record['incident_state'] in {'Resolved', 'Cancelled'} and list_id != CLOSED_LIST_ID:
        print("%s status mismatch - %s / %s" % (record['number'], record['incident_state'], list_lookup[list_id].name))
