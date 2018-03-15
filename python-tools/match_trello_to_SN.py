from trello import TrelloClient
from pprint import pprint
from inspect import getmembers
from datetime import datetime
import json
import csv
from os import path
from trello_secrets import *

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
    api_key=TRELLO_SECRETS['api_key'],
    api_secret=TRELLO_SECRETS['api_secret'],
    token=TRELLO_SECRETS['token'],
    token_secret=TRELLO_SECRETS['token_secret']
)

xref_dict = {}
list_lookup = {}

servicenow_dump = read_servicenow_file()

backlog_board = client.get_board(TRELLO_IDS.BOARDS.BACKLOG)
inwork_board = client.get_board(TRELLO_IDS.BOARDS.INWORK)

issow_lists = inwork_board.all_lists( ) + backlog_board.all_lists( )

for list in issow_lists:
    list_lookup[list.id] = list

#issow_cards = trello.boards.get_card(ISSOW_BOARD_ID,None,None,None,None,None,"all","idList,name,url,labels,closed")
all_cards = inwork_board.all_cards( ) + backlog_board.all_cards( ) 
for card in all_cards:
    incident_number = card.name.partition('-')[0].strip()
    xref_dict[incident_number] = card 

    if incident_number not in servicenow_dump['dict'] and card.idList != TRELLO_IDS.LISTS.RESOLVED:
        print("%s missing in service now export - list %s" % (incident_number, list_lookup[card.idList].name))
        continue

    if card.closed == True:
        continue

    if card.idList == TRELLO_IDS.LISTS.RESOLVED and incident_number in servicenow_dump['dict']:
        if servicenow_dump['dict'][incident_number]['incident_state'] not in {'Resolved', 'Cancelled'}:
            print("%s closed in Trello, Status in SN = %s" % (incident_number, servicenow_dump['dict'][incident_number]['incident_state']))
           
    

for record in servicenow_dump['rows']:
    if (record['number'] not in xref_dict):
        print("%s missing in trello" % (record['number']))
        continue
    list_id = xref_dict[record['number']].idList
    if record['incident_state'] in {'Resolved', 'Cancelled'} and list_id != TRELLO_IDS.LISTS.RESOLVED:
        print("%s status mismatch - %s / %s" % (record['number'], record['incident_state'], list_lookup[list_id].name))
