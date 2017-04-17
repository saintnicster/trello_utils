from trello import TrelloApi
from pprint import pprint
from inspect import getmembers
from Mytrello import Mytrello
from datetime import datetime
import json
import csv
from os import path

def read_servicenow_file():
    file_rows = []
    sn_dict = {}
    with open('C:\\Users\\fajarn\\Documents\\backlog_importer\\incident.csv') as csv_file:
        file_reader = csv.DictReader(csv_file)
        
        for row in file_reader:
            file_rows.append(row)
            sn_dict[row['number']] = row
    return { 'rows' : file_rows, 'dict' : sn_dict }

TRELLO_APP_KEY = "***REMOVED***"
TOKEN = "***REMOVED***"
ISSOW_BOARD_ID = '587d4739aacd90eb33fedfce'
CLOSED_LIST_ID = '587fb500aa3ee04f092ccc7d'

xref_dict = {}
list_lookup = {}

servicenow_dump = read_servicenow_file()

trello = TrelloApi(TRELLO_APP_KEY, TOKEN)
trello.extras = Mytrello(TRELLO_APP_KEY, TOKEN)

issow_lists = trello.boards.get_list(ISSOW_BOARD_ID)
for list in issow_lists:
    list_lookup[list['id']] = list

issow_cards = trello.boards.get_card(ISSOW_BOARD_ID,None,None,None,None,None,"all","idList,name,url,labels,closed")
for card in issow_cards:
    incident_number = card['name'].partition('-')[0].strip()
    xref_dict[incident_number] = card 

    if incident_number not in servicenow_dump['dict'] and card['idList'] != CLOSED_LIST_ID:
        print("%s missing in service now export - list %s" % (incident_number, list_lookup[card['idList']]['name']))
        continue

    if card['closed'] == True:
        continue

    if card['idList'] == CLOSED_LIST_ID:
        if servicenow_dump['dict'][incident_number]['incident_state'] not in {'Resolved', 'Cancelled'}:
            print("%s closed in Trello, Status in SN = %s" % 
                (incident_number, servicenow_dump['dict'][incident_number]['incident_state']))
           
    

for record in servicenow_dump['rows']:
    if (record['number'] not in xref_dict):
        print("%s missing in trello" % (record['number']))
        continue

    if record['incident_state'] in {'Resolved', 'Cancelled'} and xref_dict[record['number']]['idList'] != CLOSED_LIST_ID:
        print("%s status mismatch - " % (record['number']))
