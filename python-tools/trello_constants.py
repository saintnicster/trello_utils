

TRELLO_SECRETS = {
    'api_key':      '***REMOVED***',
    'api_secret':   '***REMOVED***',
    'token':        '***REMOVED***',
    'token_secret': '***REMOVED***' }


TRELLO_IDS = type('trello_ids', 
    (object,), {
        "BOARDS" : type('board_ids',(object,), { "BACKLOG" : '587d4739aacd90eb33fedfce', 
                                                 "INWORK" : '59b801ead00a15fd62d1fe05' } ),
        "LISTS"  : type('list_ids' ,(object,), { "NEWLY_CREATED" : '587e244b50ed39d516edf94f', 
                                                 "NOT_BVILLE"    : '598b14d18ce45e0e70ace903', 
                                                 "RESOLVED"      : '587fb500aa3ee04f092ccc7d'} ),
        "LABELS" : type('label_ids',(object,), { "BU_PRIORITY"   : '58823fceced82109ffdda066',
                                                 "CONFIG"        : '58a46d1eced82109ff4b1165' } )
        }
    )

BU_LABELS = {
     "AP": { "name" : "[AP]LNG",   "id": '5909f067ced82109ff73e5e1', "label_obj":None },
     "AL": { "name" : "[Al]pine",  "id": '587d4927edd7e54c19c1537d', "label_obj":None },
     "B" : { "name" : "[B]Ville",  "id": '587d4928c71ad05630e1700a', "label_obj":None },
     "D" : { "name" : "[D]arwin",  "id": '587d4927c718b5056ccd5c57', "label_obj":None },
     "J" : { "name" : "[J]Area",   "id": '587d492828c911be88e947aa', "label_obj":None },
     "N" : { "name" : "[N]orway",  "id": '587d4928e58413b6db42f672', "label_obj":None },
     "S" : { "name" : "[S]uban",   "id": '587d4927ae03f523db5922e8', "label_obj":None },
     "SU": { "name" : "[Su]rmont", "id": '587d4926323a283815b8947c', "label_obj":None },
     "T" : { "name" : "[T]eeside", "id": '587d4926bfe0ba786c54918c', "label_obj":None } }