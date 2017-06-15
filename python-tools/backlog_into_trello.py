import requests
import json
import csv
from trello import TrelloApi
from pprint import pprint
from inspect import getmembers
TRELLO_COLORS = {'GREEN': 'green',
                 'YELLOW': 'yellow',
                 'ORANGE': 'orange',
                 'RED': 'red',
                 'PURPLE': 'purple',
                 'BLUE': 'blue',
                 'PINK': 'pink',
                 'SKY': 'sky',
                 'LIME': 'lime',
                 'BLACK': 'black'}

TRELLO_APP_KEY = "***REMOVED***"
TOKEN = "***REMOVED***"
ISSOW_BOARD_ID = '587d4739aacd90eb33fedfce'

trelloboard_issow = None

def read_servicenow_file():
    file_rows = []
    with open('C:\\Users\\fajarn\\Documents\\backlog_importer\\incident.csv') as csv_file:
        file_reader = csv.DictReader(csv_file)
        print(file_reader.fieldnames)
        for row in file_reader:
            file_rows.append(row)
    return file_rows


trellolabel_assignees = {}
xref_dict = {}
trello = TrelloApi(TRELLO_APP_KEY, TOKEN)
trello.extras = Mytrello(TRELLO_APP_KEY, TOKEN)
trello_token = trello.tokens.get(TOKEN)

boardList = trello.members.get_board(trello_token['idMember'])

trelloboard_issow = trello.boards.get(ISSOW_BOARD_ID)

trellolist_inprog = trello.lists.new('Awaiting Deploy?', trelloboard_issow['id'])
trellolist_estimated = trello.lists.new('Estimate Delivered', trelloboard_issow['id'])
trellolist_backlog = trello.lists.new('Awaiting Analysis', trelloboard_issow['id'])

trellolabel_onhold = trello.extras.create_label("On Hold", TRELLO_COLORS['ORANGE'], trelloboard_issow['id'])
trellolabel_inprog = trello.extras.create_label("In Progress", TRELLO_COLORS['ORANGE'], trelloboard_issow['id'])
trellolabel_assign = trello.extras.create_label("Assigned", TRELLO_COLORS['ORANGE'], trelloboard_issow['id'])
trellolabel_surmont = trello.extras.create_label("Surmont", TRELLO_COLORS['LIME'], trelloboard_issow['id'])
trellolabel_teeside = trello.extras.create_label("Teeside", TRELLO_COLORS['LIME'], trelloboard_issow['id'])
trellolabel_darwin = trello.extras.create_label("Darwin", TRELLO_COLORS['LIME'], trelloboard_issow['id'])
trellolabel_suban = trello.extras.create_label("Suban", TRELLO_COLORS['LIME'], trelloboard_issow['id'])
trellolabel_alpine = trello.extras.create_label("Alpine", TRELLO_COLORS['LIME'], trelloboard_issow['id'])
trellolabel_jarea = trello.extras.create_label("UK (JArea)", TRELLO_COLORS['LIME'], trelloboard_issow['id'])
trellolabel_norway = trello.extras.create_label("Norway", TRELLO_COLORS['LIME'], trelloboard_issow['id'])
trellolabel_internal = trello.extras.create_label("BVille (internal ticket)", TRELLO_COLORS['LIME'], trelloboard_issow['id'])

for incident in read_servicenow_file():
    if incident['assigned_to'] == '':
        incident['assigned_to'] = 'UNASSIGNED'
    
    if incident['assigned_to'] not in trellolabel_assignees:
        trellolabel_assignees[incident['assigned_to']] = None
        trellolabel_assignees[incident['assigned_to']] = trello.extras.create_label(incident['assigned_to'],
                                                                                    TRELLO_COLORS['BLUE'],
                                                                                    trelloboard_issow['id'])

    incident['assigned_to_label'] = trellolabel_assignees[incident['assigned_to']]

    if incident['caller_id.u_work_location.u_support_area'] == 'Alaska':
        incident['location_label'] = trellolabel_alpine
    elif incident['caller_id.u_work_location.u_support_area'] in ('AUSTRALIA (ABU West)',
                                                                  'Brisbane (ABU East)'):
        incident['location_label'] = trellolabel_darwin
    elif incident['caller_id.u_work_location.u_support_area'] == 'UK Teesside':
        incident['location_label'] = trellolabel_teeside
    elif incident['caller_id.u_work_location.u_support_area'] == 'UK Aberdeen':
        incident['location_label'] = trellolabel_jarea
    elif incident['caller_id.u_work_location.u_support_area'] == 'JAKARTA':
        incident['location_label'] = trellolabel_suban
    elif incident['caller_id.u_work_location.u_support_area'] == 'Norway':
        incident['location_label'] = trellolabel_norway
    elif incident['caller_id.u_work_location.u_support_area'] == 'Surmont':
        incident['location_label'] = trellolabel_surmont
    elif incident['caller_id.u_work_location.u_support_area'] == 'Bartlesville':
        incident['location_label'] = trellolabel_internal
    else:
        pprint(incident['caller_id.u_work_location.u_support_area'])

    if incident['incident_state'] == 'On Hold':
        incident['incident_state_label'] = trellolabel_onhold
    elif incident['incident_state'] == 'In Progress':
        incident['incident_state_label'] = trellolabel_inprog
    elif incident['incident_state'] == 'Assigned':
        incident['incident_state_label'] = trellolabel_assign
    else:
        pprint(incident['incident_state'])

    incident['trello_list'] = trellolist_backlog
    if incident['u_estimated_time_hours'] != '':
        incident['trello_list'] = trellolist_estimated
    if incident['assignment_group'] == 'SD_GLOBAL_APPS_SAP ISSOW TECH':
        incident['trello_list'] = trellolist_inprog

    incident['trello_card'] = trello.cards.new("%s - %s" % (incident['number'],
                                                            incident['short_description']),
                                               incident['trello_list']['id'],
                                               incident['description'])

    trello.extras.assign_label_to_card(incident['trello_card']['id'], incident['location_label']['id'])
    trello.extras.assign_label_to_card(incident['trello_card']['id'], incident['assigned_to_label']['id'])
    trello.extras.assign_label_to_card(incident['trello_card']['id'], incident['incident_state_label']['id'])
    trello.cards.new_attachment(incident['trello_card']['id'],
                                "https://conocophillips.service-now.com/nav_to.do?uri=incident.do?sysparm_query=number=%s" % (incident['number']),
                                "ServiceNow Incident")
    if incident['u_estimated_time_hours'] != '':
        trello.cards.new_action_comment(incident['trello_card']['id'],
                                        "Estimated at %s hours" %
                                        (incident['u_estimated_time_hours']))

    xref_dict[incident['number']] = incident['trello_card']['id']
    print("%s - %s => %s (%s)" % (incident['number'],
                                  incident['short_description'],
                                  incident['trello_card']['id'],
                                  incident['trello_list']['name']))

with open('trello-servicenow-xref.json', 'w') as xref_outfile:
    json.dump(xref_dict, xref_outfile)

