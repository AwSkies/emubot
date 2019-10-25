import json
import os.path

class Utils(object):
    def __init__(self):
        self.EMUPRICE = 500
        self.MAXEMUS = 20
        self.MAXDEFENSE = 5
        self.MAXATTACK = 2 * self.MAXDEFENSE
        self.CREDITSPEMUATK = self.EMUPRICE + 200
        self.ATTACKCOOLDOWN = 14400.0
        self.ALL_VALUE_TYPES = ['credits', 'storage', 'defense']
        self.ASKEDFORBUYEMU = dict()
        self.ASKEDFORRESET = dict()
        self.SPAMCATCH = dict()
        self.ATTACKTIMERCATCH = dict()
    
    def add_stats(self, user_id: int, amount: int, valuetype: str):
        if not valuetype in self.ALL_VALUE_TYPES:
            raise TypeError("valuetype must be " + ', '.join(self.ALL_VALUE_TYPES))
        if os.path.isfile("users.json"):
            try:
                with open('users.json', 'r') as fp:
                    users = json.load(fp)
                users[user_id][valuetype] += amount
                with open('users.json', 'w') as fp:
                    json.dump(users, fp, sort_keys=True, indent=4)
            except KeyError:
                with open('users.json', 'r') as fp:
                    users = json.load(fp)
                users[user_id] = {}
                #users[user_id][valuetype] = amount
                for vt in self.ALL_VALUE_TYPES:
                    if vt == valuetype:
                        users[user_id][valuetype] = amount
                    else:
                        users[user_id][valuetype] = 0
                with open('users.json', 'w') as fp:
                    json.dump(users, fp, sort_keys=True, indent=4)
        else:
            users = {user_id: {}}
            users[user_id][valuetype] = amount
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
    
    def get_stats(self, user_id: int, valuetype: str):
        if not valuetype in self.ALL_VALUE_TYPES:
            raise TypeError("valuetype must be " + ', '.join(self.ALL_VALUE_TYPES))
        if os.path.isfile('users.json'):
            try:
                with open('users.json', 'r') as fp:
                    users = json.load(fp)
                return users[user_id][valuetype]
            except KeyError:
                with open('users.json', 'r') as fp:
                    users = json.load(fp)
                users[user_id] = {}
                users[user_id][valuetype] = 0
                return 0
        else:
            return 0
        
    def spamswitch(self, authorid):
        self.SPAMCATCH[authorid] = False    
    
    def attackswitch(self, authorid):
        self.ATTACKTIMERCATCH[authorid] = False
    
