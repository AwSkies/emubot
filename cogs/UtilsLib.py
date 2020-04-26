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
        self.ASKEDFORDISABLESTATS = dict()
        self.SPAMCATCH = dict()
        self.ATTACKED = dict()
        self.GAMBLEINFO = dict()
    
    #normal stats manipulation -----------------------------------------
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
            
    #disabled users manipulation ---------------------------------------
    def get_disabled(self):
        if os.path.isfile('disabled.json'):
            with open('disabled.json', 'r') as f:
                return json.load(f)
        else:
            return []
            
    def is_disabled(self, user_id: int):
        if user_id in self.get_disabled():
            return True
        else:
            return False
            
    def add_disabled(self, user_id: int):
        if self.is_disabled(user_id):
            raise RuntimeError('user is already disabled')
        else:
            if os.path.isfile('disabled.json'):
                with open('disabled.json', 'r') as f:
                    disabled = json.load(f)
                    disabled += [user_id]
                    with open('disabled.json', 'w') as f:
                        json.dump(disabled, f, sort_keys = True, indent = 4)
            else:
                with open('disabled.json', 'w') as f:
                    json.dump([user_id], f, sort_keys = True, indent = 4)
                
    def remove_disabed(self, user_id: int):
        if os.path.isfile('disabled.json'):
            if not self.is_disabled(user_id):
                raise RuntimeError('user is not disabled')
            else:
                with open('disabled.json', 'r') as f:
                    disabled = json.load(f)
                disabled.remove(user_id)
                with open('disabled.json', 'w') as f:
                    json.dump(disabled, f, sort_keys = True, indent = 4)
        
    #cooldown switch for earning stats through chatting
    def spamswitch(self, authorid):
        self.SPAMCATCH[authorid] = False
