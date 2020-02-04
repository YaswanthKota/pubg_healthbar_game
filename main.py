from classes.game import person,bcolors
from classes.magic import spell
from classes.inventory import items
import random

# create black magic
fire = spell("fire",25,600,"black")
thunder = spell("thunder",25,600,"black")
blizard = spell("blizard",25,600,"black")
meteor = spell("meteor",40,1200,"black")
quake = spell("quake",14,400,"black")

# create white magic
cure= spell("cure",25,620,"white")
cura= spell("cura",35,1500,"white")
curaga=spell("curaga",50,6000,"white")

# create some items
Potion = items("Potion","potion","Heals 50 Hp",50)
Hipotion = items("Hipotion","potion","Heals 100 Hp",100)
Superpotion = items("Superpotion","potion","Heals 500 Hp",1000)
Elixer = items("Elixer","elixer","Fully Restores HP/MP of one party member",9999)
Hielixer = items("Mega-elixer","elixer","Fully restores party's Hp/Mp",9999)
Greenade = items("Greenade","attack","Deals 500 damage",500)

player_spells=[fire,thunder,blizard,meteor,quake,cure,cura]
enemy_spells=[meteor,curaga,fire]
player_items=[{"item" : Potion, "quantity" : 15},{"item" : Hipotion, "quantity" : 5},
              {"item" : Superpotion, "quantity" : 5},{"item" : Elixer, "quantity" : 5},
              {"item" : Hielixer, "quantity" : 2},{"item" : Greenade, "quantity" : 5}]
#instantiate people
player1 =person("Yaswanth:",4060,185,300,34,player_spells,player_items)
player2 =person("Ravi:    ",3960,155,310,34,player_spells,player_items)
player3 =person("Anirudh: ",3860,165,288,34,player_spells,player_items)

enemy1 =person("Ravan    ",18000,705,525,25,enemy_spells,[])
enemy2 =person("Titla    ",1100,130,560,325,enemy_spells,[])
enemy3 =person("Bhaladeva",1200,120,315,25,enemy_spells,[])
enemies=[enemy1,enemy2,enemy3]
players=[player1,player2,player3]

running= True
i=0
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!!!" + bcolors.ENDC)
while running:
       print("==================================")

       print("\n\n")
       print("NAME                          HP                                          MP ")
       for player in players:
              player.stats()
       print("\n")
       for enemy in enemies:
              enemy.get_enemy_stats()


       for player in players:

              player.choose_action()
              choice=input("    choose action:")
              index= int(choice)-1

              if index == 0 :
                     dmg = player.generate_damage()
                     enemy =player.choose_target(enemies)
                     enemies[enemy].take_damage(dmg)
                     print("You attacked "+ enemies[enemy].name.replace(" ","") +" for",dmg,"Points of damage")

                     if enemies[enemy].get_hp()==0:
                            print(enemies[enemy].name.replace(" ","")+" has died.")
                            del enemies[enemy]
              elif index == 1 :
                     player.choose_magic()
                     magic_choice = int(input("    choose magic")) -1
                     if magic_choice == -1:
                            continue

                     spell = player.magic[magic_choice]
                     magic_dmg=spell.generate_damage()

                     current_mp= player.get_mp()
                     if spell.cost > current_mp:
                            print(bcolors.FAIL+"\n not enough mp\n"+bcolors.ENDC)
                            continue
                     player.reduce_mp(spell.cost)

                     if spell.type =="white":
                            player.heal(magic_dmg)
                            print(bcolors.OKBLUE + "\n"+ spell.name + " heals for" ,str(magic_dmg),"HP"+ bcolors.ENDC)
                     elif spell.type =="black":
                            enemy = player.choose_target(enemies)
                            enemies[enemy].take_damage(magic_dmg)
                            print(bcolors.OKBLUE +"\n" + spell.name + " deals",str(magic_dmg), "point of damage to"+enemies[enemy].name.replace(" ","")+ bcolors.ENDC)
                            if enemies[enemy].get_hp() == 0:
                                   print(enemies[enemy].name.replace(" ","") + "has died.")
                                   del enemies[enemy]

              elif index == 2:
                    player.choose_item()
                    item_choice=int(input("    choose Item: ")) -1
                    if item_choice == -1:
                           continue

                    item = player.items[item_choice]["item"]

                    if player.items[item_choice]["quantity"] == 0:
                           print(bcolors.FAIL+"\n"+"None left..."+bcolors.ENDC)
                           continue
                    player.items[item_choice]["quantity"] -=1


                    if item.type =="potion":
                           player.heal(item.prop)
                           print(bcolors.OKGREEN+"\n"+ item.name+" Heals for",str(item.prop),"HP"+bcolors.ENDC )
                    elif item.type== "elixer":
                           if item.name=="mega-elixer":
                                  for i in players:
                                         i.hp=i.maxhp
                                         i.mp=i.maxmp
                           else:
                                  player.hp = player.maxhp
                                  player.mp = player.maxmp
                           print(bcolors.OKGREEN+"\n"+item.name+"fully restores the hp/mp"+bcolors.ENDC)
                    elif item.type=="attack":
                           enemy = player.choose_target(enemies)
                           enemies[enemy].take_damage(item.prop)
                           print(bcolors.FAIL+"\n"+item.name+"deals",str(item.prop),"point of damage to "+enemies[enemy].name+bcolors.ENDC)
                           if enemies[enemy].get_hp() == 0:
                                  print(enemies[enemy].name.replace(" ","") + " has died.")
                                  del enemies[enemy]
       #check if battle is over
       defeated_enemies=0
       defeated_players=0
       for enemy in enemies:
              if enemy.get_hp()==0:
                     defeated_enemies+=1
       for player in players:
              if player.get_hp()==0:
                     defeated_players+=1

       #check if enemy own
       if defeated_enemies== 2:
              print(bcolors.OKGREEN + "you win" + bcolors.ENDC)
              running= False
       #check if player won
       elif defeated_players  == 2:
              print(bcolors.FAIL +"your enemies have defeated you! "+ bcolors.ENDC)
              running=False
       print("\n")
       #enemy attack phase
       for enemy in enemies:
              enemy_choice=random.randrange(0,2)
              if enemy_choice==0:
                     #chose attack
                     target=random.randrange(0,len(players))
                     enemy_dmg = enemies[0].generate_damage()
                     players[target].take_damage(enemy_dmg)
                     print(enemy.name.replace(" ","")+" attacks "+players[target].name.replace(" ","")+ " for" , enemy_dmg)
              elif enemy_choice==1:
                     spell,magic_dmg=enemy.choose_enemy_spell()
                     enemy.reduce_mp(spell.cost)
                     if spell.type =="white":
                            enemy.heal(magic_dmg)
                            print(bcolors.OKBLUE +"\n"+ spell.name + " heals"+enemy.name+" for" ,str(magic_dmg),"HP."+ bcolors.ENDC)
                     elif spell.type =="black":
                            target = random.randrange(0, 3)
                            players[target].take_damage(magic_dmg)
                            print(bcolors.OKBLUE +"\n" +enemy.name.replace("","")+ spell.name + " deals",str(magic_dmg), "point of damage to "+players[target].name.replace(" ","")+ bcolors.ENDC)
                            if players[target].get_hp() == 0:
                                   print(players[target].name.replace(" ","") + " has died.")
                                   del players[player]