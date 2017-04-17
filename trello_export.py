from trello import TrelloApi
from pprint import pprint
from inspect import getmembers
from Mytrello import Mytrello
from datetime import datetime
import json
import csv

TRELLO_APP_KEY = "***REMOVED***"
TOKEN = "***REMOVED***"
ISSOW_BOARD_ID = '587d4739aacd90eb33fedfce'

list_lookup = {}
csv_output = []

trello = TrelloApi(TRELLO_APP_KEY, TOKEN)
trello.extras = Mytrello(TRELLO_APP_KEY, TOKEN)

issow_lists = trello.boards.get_list(ISSOW_BOARD_ID)
for list in issow_lists:
    list_lookup[list['id']] = list

issow_cards = trello.boards.get_card(ISSOW_BOARD_ID,None,None,None,None,None,None,"idList,name,url,labels,closed")

for card in issow_cards:
    if card["closed"] == True:
        print("Card archived! %s" % card['name'])
        continue
    
    card["labelText"] = card["ServiceNow_Status"] = card["ServiceNow_Assigned"] = card["ServiceNow_BU"] = card["BU_Identified_Priority"] = ""
    
    for label in card["labels"]:
        if label['color'] == 'orange':
           card["ServiceNow_Status"] = label['name'] 
        elif label['color'] == 'blue':
            card["ServiceNow_Assigned"] = label['name'] 
        elif label['color'] == 'lime':
            card["ServiceNow_BU"] = label['name'] 
        elif label['color'] == 'red':
            card["BU_Identified_Priority"] = 'YES'
    
    csv_output.append({ "incidentName": card['name'],
                        "listName": list_lookup[card['idList']]['name'],
                        "BU_Reported": card["ServiceNow_BU"],
                        "SN_Status": card["ServiceNow_Status"],
                        "SN_Assigned": card["ServiceNow_Assigned"],
                        "BU_Identified_Priority": card["BU_Identified_Priority"] })

csv_filename = "//conoco.net/bvl_shared/temp/fajarn/trello_export/trello_export_"+datetime.now().strftime("%Y%m%d%H%M%S")+'.csv'
with open(csv_filename,'w') as csv_file:
    writer = csv.DictWriter(csv_file, ["incidentName",'listName',"BU_Reported","SN_Status", "SN_Assigned", "BU_Identified_Priority"],None,'raise','unix')
    writer.writeheader()
    for row in csv_output:
        writer.writerow(row)
