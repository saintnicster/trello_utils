from trello import TrelloClient
from pprint import pprint
from inspect import getmembers
from Mytrello import Mytrello
from datetime import datetime
import json
import csv

client = TrelloClient(
    api_key='***REMOVED***',
    api_secret='***REMOVED***',
    token='cf7bc847fedeedd732c113b2f6792dbcb8ac97df62498a8a8ba58a16655a54ee',
    token_secret='***REMOVED***'
)

ISSOW_BOARD_ID = '587d4739aacd90eb33fedfce'

list_lookup = {}
csv_output = []
issow_board = client.get_board(ISSOW_BOARD_ID)
issow_lists = issow_board.all_lists( )
all_cards = issow_board.open_cards( )

for list in issow_lists:
    list_lookup[list.id] = list

for card in all_cards:
    if card.closed == True:
        print("Card archived! %s" % card.name)
        continue
    
    card.labelText = card.ServiceNow_Status = card.ServiceNow_Assigned = card.ServiceNow_BU = card.BU_Identified_Priority = ""
    
    for label in card.list_labels:
        if label.color == 'orange':
           card.ServiceNow_Status = label.name 
        elif label.color == 'blue':
            card.ServiceNow_Assigned = label.name 
        elif label.color == 'lime':
            card.ServiceNow_BU = label.name 
        elif label.color == 'red':
            card.BU_Identified_Priority = 'YES'
    
    csv_output.append({ "incidentName": card.name,
                        "listName": list_lookup[card.idList].name,
                        "BU_Reported": card.ServiceNow_BU,
                        "SN_Status": card.ServiceNow_Status,
                        "SN_Assigned": card.ServiceNow_Assigned,
                        "BU_Identified_Priority": card.BU_Identified_Priority })

csv_filename = "//conoco.net/bvl_shared/temp/fajarn/trello_export_"+datetime.now().strftime("%Y%m%d%H%M%S")+'.csv'
with open(csv_filename,'w') as csv_file:
    writer = csv.DictWriter(csv_file, ["incidentName",'listName',"BU_Reported","SN_Status", "SN_Assigned", "BU_Identified_Priority"],None,'raise','unix')
    writer.writeheader()
    for row in csv_output:
        writer.writerow(row)
