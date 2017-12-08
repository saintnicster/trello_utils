from trello import TrelloClient
from trello import Label as TrelloLabel
from pprint import pprint
from inspect import getmembers

import pyperclip

TRELLO_IDS = type('trello_ids', 
    (object,), {
        "BOARDS" : type('board_ids',(object,), { "BACKLOG" : '587d4739aacd90eb33fedfce', "INWORK" : '59b801ead00a15fd62d1fe05' } ),
        "LISTS"  : type('list_ids' ,(object,), { "NEWLY_CREATED" : '587e244b50ed39d516edf94f', "NOT_BVILLE" : '598b14d18ce45e0e70ace903', "RESOLVED" : '587fb500aa3ee04f092ccc7d'} ),
        "LABELS" : type('label_ids',(object,), { "BU_PRIORITY" : '58823fceced82109ffdda066',"CONFIG" : '58a46d1eced82109ff4b1165' } )
        }
    )

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

list_created = client.get_board(TRELLO_IDS.BOARDS.BACKLOG).get_list(TRELLO_IDS.LISTS.NEWLY_CREATED)

def create_trello_ticket():
    while True:
        print("New incident into trello")
        #sn_num_input = input("** SN Incident Number - ")
        sn_num_input = "INC3139012"
        sn_num_input.strip()
        if len(sn_num_input) == 0:
            return False
        else:
            if sn_num_input[0:3] != "INC":
                sn_num_input = "INC"+sn_num_input
            
            if len(client.search(sn_num_input, False, [], TRELLO_IDS.BOARDS.BACKLOG+','+TRELLO_IDS.BOARDS.INWORK )) != 0:
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
            break

    while True:
        config_input = input("** Is this a config change? [y/n] ").upper()
        if config_input not in ["Y", "N"]:
            print("Invalid input... try again\n %s" % (config_input))
        else:
            break

    while True:
        input("\nCopy Long description into clipboard.  Press ENTER to continue")
        description_input = pyperclip.paste()
        
        print("Description found - \n%s" % (description_input))
        if input("Is this correct? [y/n] ").upper() == 'Y':
            break

    while True:
        resolved_input = input("** Has this already been resolved? [y/n] ").upper()
        if resolved_input not in ["Y", "N"]:
            print("Invalid input... try again\n %s" % (resolved_input))
        else:
            break

    while True:
        bville_input = input("** Is this being handled by Bartlesville support team? [y/n] ").upper()
        if bville_input not in ["Y", "N"]:
            print("Invalid input... try again\n %s" % (resolved_input))
        else:
            break

    if bu_label["label_obj"] == None:
        bu_label["label_obj"] = TrelloLabel(client, bu_label["id"], None, None).fetch()
    
    card_labels = [ bu_label["label_obj"] ]
    if priority_input == 'Y':
        card_labels.append( TrelloLabel(client, TRELLO_IDS.LABELS.BU_PRIORITY, None, None).fetch() )

    if config_input == 'Y':
        card_labels.append( TrelloLabel(client, TRELLO_IDS.LABELS.CONFIG, None, None).fetch() )

    new_card = list_created.add_card(  "%s - %s" % (sn_num_input, short_descr_input,), description_input, card_labels )

    new_card.attach("ServiceNow - %s" % (sn_num_input), None, None, 
                    "https://conocophillips.service-now.com/nav_to.do?uri=incident.do?sysparm_query=number=%s" % (sn_num_input))
                    
    if bville_input == 'N':
        new_card.change_list( TRELLO_IDS.LISTS.NOT_BVILLE )

    if resolved_input == 'Y':
        new_card.change_board( TRELLO_IDS.BOARDS.INWORK, TRELLO_IDS.LISTS.RESOLVED)
    
    print("Card created at url %s" % (new_card.url))

    


while True:
    if create_trello_ticket() == False:
        input("No input found, press any key to exit")
        break