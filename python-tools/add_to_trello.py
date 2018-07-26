from trello import trelloclient
from trello import Label as TrelloLabel
from pprint import pprint
from inspect import getmembers
import pyperclip
from issow_trello_setup import *

bu_names = []
for bu in BU_LOOKUP.items() :
    bu_names.append( bu[1]["name"] )

list_created = ISSOW_TRELLO_CLIENT.get_board(TRELLO_IDS.BOARDS.BACKLOG).get_list(TRELLO_IDS.LISTS.NEWLY_CREATED)

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
            
            if len(ISSOW_TRELLO_CLIENT.search(sn_num_input, False, [], TRELLO_IDS.BOARDS.BACKLOG+','+TRELLO_IDS.BOARDS.INWORK )) != 0:
                print("Incident %s already in Trello\n\n" % (sn_num_input) )
            else:
                break
    
    short_descr_input = input("** SN Short Description - ")

    while True:
        bu_input = input("** Business Unit?\n%s - " % (', '.join(bu_names))).upper()
        if bu_input not in list(BU_LOOKUP):
            print("BU not recognized.  Try again...\n")
        else:
            bu_label = BU_LOOKUP[bu_input]
            break
    
    while True:
        priority_input = input("** Is this a BU priority? [y/n] ").upper()
        if priority_input not in ["Y", "N"]:
            print("Invalid input... try again\n %s" % (priority_input))
        else:
            break

    while True:
        bville_input = input("** Is this being handled by Bartlesville support team? [y/n] ").upper()
        if bville_input not in ["Y", "N"]:
            print("Invalid input... try again\n %s" % (bville_input))
        else:
            break

    while True:
        techteam_input = input("** Is this a ticket for the Tech Team? [y/n] ").upper()
        if techteam_input not in ["Y", "N"]:
            print("Invalid input... try again\n %s" % (resolved_input))
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

    if bu_label["label_obj"] == None:
        bu_label["label_obj"] = TrelloLabel(ISSOW_TRELLO_CLIENT, bu_label["id"], None, None).fetch()
    
    card_labels = [ bu_label["label_obj"] ]
    if priority_input == 'Y':
        card_labels.append( TrelloLabel(ISSOW_TRELLO_CLIENT, TRELLO_IDS.LABELS.BU_PRIORITY, None, None).fetch() )

    if config_input == 'Y':
        card_labels.append( TrelloLabel(ISSOW_TRELLO_CLIENT, TRELLO_IDS.LABELS.CONFIG, None, None).fetch() )

    
    if techteam_input == 'Y':
        title_pattern = "%s - TECH TEAM - %s"
    else:
        title_pattern = "%s - %s"

    new_card = list_created.add_card(  title_pattern % (sn_num_input, short_descr_input,), description_input, card_labels )

    new_card.attach("ServiceNow - %s" % (sn_num_input), None, None, 
                    "https://conocophillips.service-now.com/nav_to.do?uri=incident.do?sysparm_query=number=%s" % (sn_num_input))
                    
    if bville_input == 'N':
        new_card.change_list( TRELLO_IDS.LISTS.NOT_BVILLE )

    if techteam_input == 'Y':
        new_card.change_board( TRELLO_IDS.BOARDS.INWORK, TRELLO_IDS.LISTS.TECH_TEAM )

    if resolved_input == 'Y':
        new_card.change_board( TRELLO_IDS.BOARDS.INWORK, TRELLO_IDS.LISTS.RESOLVED )
    
    print("Card created at url %s" % (new_card.url))

while True:
    if create_trello_ticket() == False:
        input("No input found, press any key to exit")
        break