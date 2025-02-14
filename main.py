from game import prson, bcolors
from magic import Spell
from inventory import Item
import random

# black magic
#======(self, name, cost, dmg, type )
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# white magic
cure = Spell("cure", 12, 120, "white")
cura = Spell("cura", 18, 200, "white")
curaga = Spell("curaga", 50 , 6000, "white")

# create some Items(name , type , describtion, prop)
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion","Heals 100 HP", 100 )
superpotion = Item("Super potion", "potion","Heals 500 HP", 500)

elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999 )
hielixir = Item("MegaElixir", "elixir","Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spell = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spell = [fire, meteor, curaga]
player_items = [{"item" : potion,"quantity" : 15 },{"item" : hipotion,"quantity" : 5 } ,
                {"item" : superpotion,"quantity" : 5 },{"item" : elixir,"quantity" : 5 },
                {"item" : hielixir,"quantity" : 2 },{"item" : grenade,"quantity" : 5 }]
#  def __init__(hp, mp, atk, df, magic):
player1 = prson("Valos:",150, 50, 60, 34, player_spell , player_items)
player2 = prson("Nick :",4290, 50, 60, 34, player_spell , player_items)
player3 = prson("Robot:",5000, 50, 60, 34, player_spell , player_items)

enemy1 = prson("Imp1 :", 1250, 130, 560, 325, enemy_spell , [])
enemy2 = prson("Magus:",1500, 40, 45, 25, enemy_spell , [])
enemy3 = prson("Imp2 :", 125, 130, 560, 325, enemy_spell , [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKED" + bcolors.ENDC)

while running:
    print("============================")

    print("\n\n")
    print("NAME                       HP                                        MP")
    for player in players:
        player.get_stats()

    for enemy in enemies:
        enemy.get_stats()
    
    print("\n")

    for player in players:

        player.choose_action()
        choice = input("    choose action:" )
        index = int(choice) - 1


        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies) 

            enemies[enemy].take_damage(dmg)
            print( player.get_name().replace(':','')+" attacked for", dmg, "points of damage to "+ enemies[enemy].name.replace(":","") )
            
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + "has died.")
                del enemies[enemy]

        elif index == 1:  #magic choice player
            dmg = player.choose_magic()
            magic_choice = int(input("    choose magic:"))-1

            if magic_choice == -1 :
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)
                            

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name +" heals for "+ str(magic_dmg), "HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg) 
                print(bcolors.OKBLUE + "\n" + spell.name +" deals "+ str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(":","") + bcolors.ENDC)        
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + "has died.")
                    del enemies[enemy]
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item:")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]  

            if player.items[item_choice]["quantity"] == 0:
                print("\n" + bcolors.FAIL + bcolors.BOLD + "None left ..."+ bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) , "HP" + bcolors.ENDC)
            elif item.type == "elixir":

                if item.name == "MegaElixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp  
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) , " points of damage to " + enemies[enemy].name.replace(":","") + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + "has died.")
                    del enemies[enemy]

    print("------------------------------------")
    
    if  len(enemies)== 1:
        print(bcolors.OKGREEN + "you guys win \U0001F601"+ bcolors.ENDC)
        running = False
    elif len(players) == 1:
        print(bcolors.FAIL + "your enemies have deafeted you! \U0001F60F"+ bcolors.ENDC)
        running = False

    print("\n")
    #Enemy attack at any circumstances:
    for enemy in enemies:
        enemy_choice = random.randrange(0,2)

        if enemy_choice == 0 :
            player = random.randrange(0, len(players))
            enemy_dmg = enemy.generate_damage()
            players[player].take_damage(enemy_dmg)
            print(enemy.name.replace(":","") + " attacks for", enemy_dmg, "to player", players[player].name.replace(":",""))
        
        elif enemy_choice == 1 :
            spell, magic_dmg = enemy.choose_enemy_spell()
            print("type:", spell.type)

            current_mp = enemy.get_mp()
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue
            
            enemy.reduce_mp(spell.cost)
                            
            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + enemy.name.replace(":","") + " chose: " + spell.name +" heals for "+ str(magic_dmg), "HP" + bcolors.ENDC)
            elif spell.type == "black":
                player_target = random.randrange(0,len(players))
                players[player_target].take_damage(magic_dmg) 
                print(bcolors.OKBLUE + enemy.name.replace(":","") + " chose: " + spell.name +" deals "+ str(magic_dmg), "points of damage to " + players[player_target].name.replace(":","") + bcolors.ENDC)        
                if players[player_target].get_hp() == 0:
                    print(players[player_target].name + "has died.")
                    del players[player_target]


