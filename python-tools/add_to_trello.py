from trello import TrelloClient
from trello import Label as TrelloLabel
from pprint import pprint
from inspect import getmembers

import pyperclip

ISSOW_BOARD_ID        = '587d4739aacd90eb33fedfce'
NEWLY_CREATED_LIST_ID = '587e244b50ed39d516edf94f'
LABEL_ID_PRIORITY     = '58823fceced82109ffdda066'

BU_TRELLO_LABELS = {
     "AP": { "name" : "[AP]LNG",   "id": '5909f067ced82109ff73e5e1', "label_obj":None },
     "AL": { "name" : "[Al]pine",  "id": '587d4927edd7e54c19c1537d', "label_obj":None },
     "B" : { "name" : "[B]Ville",  "id": '587d4928c71ad05630e1700a', "label_obj":None },
     "D" : { "name" : "[D]arwin",  "id": '587d4927c718b5056ccd5c57', "label_obj":None },
     "J" : { "name" : "[J]Area",   "id": '587d492828c911be88e947aa', "label_obj":None },
     "N" : { "name" : "[N]orway",  "id": '587d4928e58413b6db42f672', "label_obj":None },
     "S" : { "name" : "[S]uban",   "id": '587d4927ae03f523db5922e8', "label_obj":None },
     "SU": { "name" : "[Su]rmont", "id": '587d4926323a283815b8947c', "label_obj":None },
     "T" : { "name" : "[T]eeside", "id": '587d4926bfe0ba786c54918c', "label_obj":None } }

client = TrelloClient(
    api_key='***REMOVED***',
    api_secret='***REMOVED***',
    token='***REMOVED***',
    token_secret='***REMOVED***'
)

bu_names = []
for bu in BU_TRELLO_LABELS.items() :
    bu_names.append( bu[1]["name"] )

def create_trello_ticket():
    while True:
        print("New incident into trello")
        sn_num_input = input("** SN Incident Number - ")
        sn_num_input.strip()
        if len(sn_num_input) == 0:
            return False
        else:
            if sn_num_input[0:3] != "INC":
                sn_num_input = "INC"+sn_num_input
            
            if len(client.search(sn_num_input, False, [], ISSOW_BOARD_ID )) != 0:
                print("Incident %s already in Trello\n\n" % (sn_num_input) )
            else:
                break
    
    short_descr_input = input("** SN Short Description - ")

    while True:
        bu_input = input("** Business Unit?\n%s - " % (', '.join(bu_names))).upper()
        if bu_input not in list(BU_TRELLO_LABELS):
            print("BU not recognized.  Try again...\n")
        else:
            bu_label = BU_TRELLO_LABELS[bu_input]
            break
    
    while True:
        priority_input = input("** Is this a BU priority? [y/n] ").upper()
        if priority_input not in ["Y", "N"]:
            print("Invalid input... try again\n %s" % (priority_input))
        else:
            priority = TrelloLabel(client, bu_label["id"], None, None).fetch()
            break

    while True:
        input("\nCopy Long description into clipboard.  Press ENTER to continue")
        description_input = pyperclip.paste()
        
        print("Description found - \n%s" % (description_input))
        if input("Is this correct? [y/n] ").upper() == 'Y':
            break


    list_created = client.get_board(ISSOW_BOARD_ID).get_list(NEWLY_CREATED_LIST_ID)

    if bu_label["label_obj"] == None:
        bu_label["label_obj"] = TrelloLabel(client, bu_label["id"], None, None).fetch()
    
    card_labels = [ bu_label["label_obj"] ]
    if priority_input == 'Y':
        card_labels.append( TrelloLabel(client, LABEL_ID_PRIORITY, None, None).fetch() )

    new_card = list_created.add_card(  "%s - %s" % (sn_num_input, short_descr_input,), description_input, card_labels )
    new_card.attach("ServiceNow - %s" % (sn_num_input), None, None, 
                    "https://conocophillips.service-now.com/nav_to.do?uri=incident.do?sysparm_query=number=%s" % (sn_num_input))
    print("Card created at url %s" % (new_card.url))


while True:
    if create_trello_ticket() == False:
        print("No input found, exiting...")
        break