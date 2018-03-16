import trello_api_stuff 
from trello import TrelloClient

TRELLO_SECRETS = trello_api_stuff.TRELLO_SECRETS

TRELLO_IDS = type('trello_ids', 
    (object,), {
        "BOARDS" : type('board_ids',(object,), { "BACKLOG" : '587d4739aacd90eb33fedfce', 
                                                 "INWORK" : '59b801ead00a15fd62d1fe05' } ),
        "LISTS"  : type('list_ids' ,(object,), { "NEWLY_CREATED" : '587e244b50ed39d516edf94f', 
                                                 "NOT_BVILLE"    : '598b14d18ce45e0e70ace903', 
                                                 "RESOLVED"      : '587fb500aa3ee04f092ccc7d'} ),
        "LABELS" : type('label_ids',(object,), { "BU_PRIORITY"   : '58823fceced82109ffdda066',
                                                 "CONFIG"        : '58a46d1eced82109ff4b1165' } ),
        "BU"    : type('bu_ids'    ,(object,), { "APLNG"       : '5909f067ced82109ff73e5e1',
                                                 "Alpine"      : '587d4927edd7e54c19c1537d',
                                                 "BVille"      : '587d4928c71ad05630e1700a',
                                                 "Darwin"      : '587d4927c718b5056ccd5c57',
                                                 "JArea"       : '587d492828c911be88e947aa',
                                                 "Norway"      : '587d4928e58413b6db42f672',
                                                 "Suban"       : '587d4927ae03f523db5922e8',
                                                 "Surmont"     : '587d4926323a283815b8947c',
                                                 "Teeside"     : '587d4926bfe0ba786c54918c'} )
        }
    )

BU_LOOKUP = {
     "AP": { "name" : "[AP]LNG",   "id": TRELLO_IDS.BU.APLNG,   "label_obj":None },
     "AL": { "name" : "[Al]pine",  "id": TRELLO_IDS.BU.Alpine,  "label_obj":None },
     "B" : { "name" : "[B]Ville",  "id": TRELLO_IDS.BU.BVille,  "label_obj":None },
     "D" : { "name" : "[D]arwin",  "id": TRELLO_IDS.BU.Darwin,  "label_obj":None },
     "J" : { "name" : "[J]Area",   "id": TRELLO_IDS.BU.JArea,   "label_obj":None },
     "N" : { "name" : "[N]orway",  "id": TRELLO_IDS.BU.Norway,  "label_obj":None },
     "S" : { "name" : "[S]uban",   "id": TRELLO_IDS.BU.Suban,   "label_obj":None },
     "SU": { "name" : "[Su]rmont", "id": TRELLO_IDS.BU.Surmont, "label_obj":None },
     "T" : { "name" : "[T]eeside", "id": TRELLO_IDS.BU.Teeside, "label_obj":None } }

ISSOW_TRELLO_CLIENT = TrelloClient(
    api_key=TRELLO_SECRETS['api_key'],
    api_secret=TRELLO_SECRETS['api_secret'],
    token=TRELLO_SECRETS['token']
)