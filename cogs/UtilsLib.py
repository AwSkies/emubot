import json
import os.path

class Utils(object):
    ATTACKCOOLDOWN = 14400.0
    def __init__(self):
        self.EMUPRICE = 500
        self.EMUSELLPRICE = 400
        self.MAXEMUS = 20
        self.MAXDEFENSE = 5
        self.MAXATTACK = 2 * self.MAXDEFENSE
        self.CREDITSPEMUATK = self.EMUPRICE + 200
        self.ALL_VALUE_TYPES = ['credits', 'storage', 'defense']
        self.ASKEDFORBUYEMU = dict()
        self.ASKEDFORSELLEMU = dict()
        self.ASKEDFORRESET = dict()
        self.SPAMCATCH = dict()
        self.ATTACKED = dict()
        self.GAMBLEINFO = dict()
    
    def add_stats(self, user_id: str, amount: int, valuetype: str):
        if not valuetype in self.ALL_VALUE_TYPES:
            raise TypeError("valuetype must be " + ', '.join(self.ALL_VALUE_TYPES))
        user_id = str(user_id)
        if user_id == str(self.bot.user.id):
            return
        if os.path.isfile("users.json"):
            try:
                with open('users.json', 'r') as fp:
                    users = json.load(fp)
                if valuetype in users[user_id]:
                    users[user_id][valuetype] += amount
                else:
                    users[user_id][valuetype] = amount
                with open('users.json', 'w') as fp:
                    json.dump(users, fp, sort_keys=True, indent=4)
            except KeyError:
                with open('users.json', 'r') as fp:
                    users = json.load(fp)
                users[user_id] = {}
                users[user_id][valuetype] = amount
                with open('users.json', 'w') as fp:
                    json.dump(users, fp, sort_keys=True, indent=4)
        else:
            users = {user_id: {}}
            users[user_id][valuetype] = amount
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
    
    def get_stats(self, user_id: str, valuetype: str):
        if not valuetype in self.ALL_VALUE_TYPES:
            raise TypeError("valuetype must be " + ', '.join(self.ALL_VALUE_TYPES))
        user_id = str(user_id)
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
