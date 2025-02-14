import random
import numpy
from magic import Spell

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class prson:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.name= name
        self.action = ["attack", "magic", "Items"]

    def generate_damage (self):
        return random.randrange(self.atkl, self.atkh)
    
    def take_damage (self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp
    
    def heal(self, dmg):
        self.hp += dmg
        if self.hp < 0:
            self.hp = 0
        elif self.hp > self.maxhp:
            self.hp = self.maxhp
        return self.hp

    def heal_mp(self, dmg):
        self.mp += dmg
        if self.mp < 0:
            self.mp = 0
        elif self.mp > self.maxmp:
            self.mp = self.maxmp
        return self.mp
        
    def get_hp(self):
        return self.hp
    
    def get_max_hp(self):
        return self.maxhp
    
    def get_mp(self):
        return self.mp
    
    def get_max_mp(self):
        return self.maxmp
    
    def get_name(self):
        return self.name
    
    def reduce_mp(self, cost):
        self.mp -= cost
        return self.mp
    
    def get_spell_name(self, i):
        return self.magic[i]["cost"]
    
    def choose_action(self):
        i = 1
        print("\n    "+ bcolors.BOLD + self.name + bcolors.ENDC)
        print("\n" + bcolors.OKBLUE + bcolors.BOLD +  "    ACTION"+ bcolors.ENDC)
        for item in self.action:
            print("        " +str(i)+":",item)
            i+=1

    def choose_magic(self):
        i=1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD +  "    MAGIC:"+ bcolors.ENDC)
        for spell in self.magic:
            print("        " + str(i) + ":", spell.name, "(cost:", str(spell.cost), ")")
            i += 1

    def choose_item(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "    ITEMS:" + bcolors.ENDC)
        for item in self.items:
            print("        " +str(i) + "." , item["item"].name , " (x", item["quantity"], ")")
            i += 1

    def choose_target(self, enemies):
        i = 1 
        print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.hp != 0:
                print("        " +str(i) + "." , enemy.name.replace(":","") , "with health point of ", enemy.hp, "/", enemy.maxhp )
                i += 1 
        choice = int(input("choose target :")) - 1
        return choice

    def get_stats(self):
        print(bcolors.BOLD + self.name + "   " ,
        str(self.hp).rjust(5," ") , "/" , str(self.maxhp).ljust(5," ") ,"  "+ bcolors.FAIL + int(numpy.ceil(self.hp*25/self.maxhp))*"❤️" + (25 - int(numpy.ceil(self.hp*25/self.maxhp)))*" " + bcolors.ENDC + bcolors.BOLD + "    " ,
        str(self.mp).rjust(3," ") , "/" , str(self.maxmp).ljust(3," ") ,"  " + bcolors.OKBLUE + int(numpy.ceil(self.mp*10/self.maxmp))*"🔮" + (10 - int(numpy.ceil(self.mp*10/self.maxmp)))*" " + bcolors.ENDC + "" )

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0,len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        pct = self.hp / self.maxhp * 100
        if spell.type == "white" and pct > 50 :
            if spell.cost > self.mp :
                return spell, magic_dmg
            else:
                return self.choose_enemy_spell()
        else:
            return spell, magic_dmg
        