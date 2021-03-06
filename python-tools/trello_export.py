from trello import TrelloClient
from pprint import pprint
from inspect import getmembers
from datetime import datetime
import json
import csv
from issow_trello_setup import *

list_lookup = {}
csv_output = []
backlog_board = ISSOW_TRELLO_CLIENT.get_board(TRELLO_IDS.BOARDS.BACKLOG)
inwork_board = ISSOW_TRELLO_CLIENT.get_board(TRELLO_IDS.BOARDS.INWORK)

issow_lists = inwork_board.all_lists( ) + backlog_board.all_lists( )
all_cards = inwork_board.open_cards(  ) + backlog_board.open_cards( )

for list in issow_lists:
    list_lookup[list.id] = list

for card in all_cards:
    if card.closed == True:
        print("Card archived! %s" % card.name)
        continue
    
    card.labelText = card.ServiceNow_Assigned = card.ServiceNow_BU = card.BU_Identified_Priority = ""
    
    for label in card.list_labels:
        if label.color == 'blue':
            card.ServiceNow_Assigned = label.name 
        elif label.color == 'green':
            card.ServiceNow_BU = label.name 
        elif label.color == 'red':
            card.BU_Identified_Priority = 'YES'

    name_partition = card.name.partition('-')
    incident_number = name_partition[0].strip()
    if incident_number.startswith('INC') == True:
        incident_name = name_partition[2].strip()
    else:
        incident_number = ''
        incident_name = card.name

    incident_name = name_partition[2].strip()

    csv_output.append({ "incidentNumber": incident_number,
                        "incidentName": incident_name,
                        "listName": list_lookup[card.idList].name,
                        "BU_Reported": card.ServiceNow_BU,
                        "SN_Assigned": card.ServiceNow_Assigned,
                        "BU_Identified_Priority": card.BU_Identified_Priority })

csv_filename = "./trello_export_"+datetime.now().strftime("%Y%m%d%H%M%S")+'.csv'
with open(csv_filename,'w') as csv_file:
    writer = csv.DictWriter(csv_file, ["incidentNumber","incidentName",'listName',"BU_Reported","SN_Assigned", "BU_Identified_Priority"],None,'raise','unix')
    writer.writeheader()
    for row in csv_output:
        writer.writerow(row)
