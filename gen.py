import numpy as np
import random

random.seed(0)

HOMEFIELD_ADVANTAGE=4
PYRO_ATK_BONUS=9
PYRO_DEF_BONUS=-9
GEO_ATK_BONUS=-9
GEO_DEF_BONUS=9
MEMORY_BONUS=7

Cryo_Necro_State=1
Pyro_A_State=1

def roll_dX(X):
 return random.choice(list(range(X)))+1

WizardPowerList={"Vita A": 19,
"Vita B": 22,
"Geo A": 21,
"Geo B": 12,
"Cryo": 23,
"Pyro A": 20,
"Pyro B": 21,
"Necro A": 22,
"Necro B": 15,
"Necro C": 13,
"Electro": 20}

def wizardPower(attacker, defender, location):
 atkPower = WizardPowerList[attacker]
 defPower = WizardPowerList[defender]
 #Apply homefield adv
 if location==attacker.split()[0]:
  atkPower+=HOMEFIELD_ADVANTAGE
 if location==defender.split()[0]:
  defPower+=HOMEFIELD_ADVANTAGE
 #Apply attack bonuses
 if attacker.split()[0]=="Geo":
  atkPower+=GEO_ATK_BONUS
 if defender.split()[0]=="Geo":
  defPower+=GEO_DEF_BONUS
 if attacker.split()[0]=="Pyro":
  atkPower+=PYRO_ATK_BONUS
 if defender.split()[0]=="Pyro":
  defPower+=PYRO_DEF_BONUS
 #Apply quirks
 #>Special detail between Vita A and Necro C
 if attacker=="Vita A" and defender=="Necro C":
  atkPower+=MEMORY_BONUS
 if attacker=="Necro C" and defender=="Vita A":
  defPower+=MEMORY_BONUS
 #>Pyro A's breakdown
 if Pyro_A_State==1:
  if defender=="Pyro A" and location=="Pyro":
   #print("yo!")
   defPower-=HOMEFIELD_ADVANTAGE
 #>Ex-mancers get HA too
 if attacker=="Geo A" and location=="Necro":
  atkPower+=HOMEFIELD_ADVANTAGE
 if attacker=="Necro B" and location=="Vita":
  atkPower+=HOMEFIELD_ADVANTAGE
 return atkPower, defPower

def wizardFight(attacker, defender, location, Cryo_Necro_State):
 atkPower, defPower = wizardPower(attacker, defender, location)
 #The Deal
 if (attacker=="Cryo" and defender=="Necro A") or (attacker=="Necro A" and defender=="Cryo"):
  if Cryo_Necro_State>1:
   return "Cryo", (Cryo_Necro_State+1)%4
  else:
   return "Necro A", (Cryo_Necro_State+1)%4
 #And for all the UN-rigged fights . . .
 ATK = atkPower+roll_dX(10)+roll_dX(10)
 DEF = defPower+roll_dX(10)+roll_dX(10)
 #print(ATK, DEF)
 if ATK>DEF:
  return attacker, Cryo_Necro_State
 else:
  return defender, Cryo_Necro_State

def wizardOdds(attacker, defender, location, Cryo_Necro_State, recordAtk=True):
 atkPower, defPower = wizardPower(attacker, defender, location)
 #The Deal
 if (attacker=="Cryo" and defender=="Necro A"):
  if Cryo_Necro_State>1:
   atkWins=10000
   defWins=0
  else:
   atkWins=0
   defWins=10000
 elif (attacker=="Necro A" and defender=="Cryo"):
  if Cryo_Necro_State>1:
   atkWins=0
   defWins=10000
  else:
   atkWins=10000
   defWins=0
 else:#And for all the UN-rigged fights . . .
  atkWins=0
  defWins=0
  for a in [1,2,3,4,5,6,7,8,9,10]:
   for b in [1,2,3,4,5,6,7,8,9,10]:
    for c in [1,2,3,4,5,6,7,8,9,10]:
     for d in [1,2,3,4,5,6,7,8,9,10]:
      if (atkPower+a+b)>(defPower+c+d):
      #if (atkPower+a)>(defPower+c):
       atkWins+=1
      else:
       defWins+=1
 if recordAtk:
  return str(atkWins/100.0)+"%"
 else:
  return str(defWins/100.0)+"%"
 
print(wizardOdds("Vita B", "Necro B", "Pyro", Cryo_Necro_State))

OurWizards = ["Vita A", "Vita B", "Geo A", "Geo B", "Cryo"]
TheirWizards = ["Pyro A", "Pyro B", "Necro A", "Necro B", "Necro C"]
TheirAttackLocations = ["Vita", "Vita", "Cryo", "Vita", "Geo"]
TheirDefenseLocations = ["Pyro", "Pyro", "Necro", "Pyro", "Necro"]

#Attack matchups

print("WE DEFEND")
titleOp="    ,"
for Wizard in OurWizards:
 titleOp+=(Wizard+", ")
print(titleOp)

for j in range(5):
 lineOp=TheirWizards[j]+", "
 for i in range(5):
  lineOp+=(wizardOdds(TheirWizards[j], OurWizards[i], TheirAttackLocations[j], Cryo_Necro_State, False) +", ")
 print lineOp

print("")
#Defense matchups

print("WE COUNTERATTACK")
titleOp="    ,"
for Wizard in OurWizards:
 titleOp+=(Wizard+", ")
print(titleOp)

for j in range(5):
 lineOp=TheirWizards[j]+", "
 for i in range(5):
  lineOp+=(wizardOdds(OurWizards[i], TheirWizards[j], TheirDefenseLocations[j], Cryo_Necro_State) +", ")
 print lineOp
print("")
#for i in range(40):
# victor, Cryo_Necro_State=wizardFight("Vita B", "Necro B", "Pyro", Cryo_Necro_State)
# print(victor)

#print("")

#for i in range(10):
 #victor, Cryo_Necro_State=wizardFight("Cryo", "Necro A", "Pyro", Cryo_Necro_State)
 #print(victor)



###########################################################################

import pandas as pd
import numpy as np

WizardPowerList={"Vita A": 19,
"Vita B": 7,
"Geo A": 21,
"Geo B": 12,
"Cryo": 23,
"Pyro A": 20,
"Pyro B": 17,
"Necro A": 22,
"Necro B": 15,
"Necro C": 13,
"Electro": 20}

Cryo_Necro_State=1
Pyro_A_State=0

Vitamancers=["Vita A", "Vita B"]
Geomancers=["Geo A", "Geo B"]
Cryomancers=["Cryo"]
Pyromancers=["Pyro A", "Pyro B"]
Necromancers=["Necro A", "Necro B"]

random.seed(0)

dictForDf = {"attacker":[], "defender":[], "location":[], "victor":[]}

vitaDf=pd.DataFrame(dictForDf)
geoDf=pd.DataFrame(dictForDf)
cryoDf=pd.DataFrame(dictForDf)
pyroDf=pd.DataFrame(dictForDf)

 

for r in range(1,1719):
 #Update people's stats here
 #Vita B keeps improving
 WizardPowerList["Vita B"]=7+r/110
 #Pyro B has his breakthrough
 if r>=652:
  WizardPowerList["Pyro B"]=9999
  if r>=671:
   WizardPowerList["Pyro B"]=21
 #Pyro A has her breakdown
 if r>=967:
  Pyro_A_State=1
  Pyromancers = ["Electro", "Pyro B"]
  if r>=979: # . . . but eventually returns to work
   Pyromancers = ["Pyro A", "Pyro B"]
 #Necro C joins, Geos hire Electro
 if r>=1101:
  Necromancers=["Necro A", "Necro B", "Necro C"]
  Geomancers=["Geo A", "Geo B", "Electro"]
  if r>=1111:
   Geomancers=["Geo A", "Geo B"]
 #Necros target everyone
 if r<503:
  attacker=random.choice(Necromancers)
  location=random.choice(["Vita", "Geo", "Geo", "Cryo", "Pyro"])
  if location=="Vita":
   defender=random.choice(Vitamancers)
   victor, Cryo_Necro_State = wizardFight(attacker, defender, location, Cryo_Necro_State)
   if r>140:
    vitaDf = vitaDf.append({"attacker":attacker, "defender":defender, "location":location, "victor":victor}, ignore_index=True)
  if location=="Geo":
   defender=random.choice(Geomancers)
   victor, Cryo_Necro_State = wizardFight(attacker, defender, location, Cryo_Necro_State)
   if r>140 or defender=="Geo B":
    geoDf = geoDf.append({"attacker":attacker, "defender":defender, "location":location, "victor":victor}, ignore_index=True)
  if location=="Cryo":
   defender=random.choice(Cryomancers)
   victor, Cryo_Necro_State = wizardFight(attacker, defender, location, Cryo_Necro_State)
   if r>140:
    cryoDf = cryoDf.append({"attacker":attacker, "defender":defender, "location":location, "victor":victor}, ignore_index=True)
  if location=="Pyro":
   defender=random.choice(Pyromancers)
   victor, Cryo_Necro_State = wizardFight(attacker, defender, location, Cryo_Necro_State)
   if r>140:
    pyroDf = pyroDf.append({"attacker":attacker, "defender":defender, "location":location, "victor":victor}, ignore_index=True)
 #Pyros vs Vitas
 elif r<954:
  #Necros are still scavenging
  attacker=random.choice(Necromancers)
  location=random.choice(["Geo", "Geo","Geo", "Cryo", "Cryo"])
  if location=="Geo":
   defender=random.choice(Geomancers)
   victor, Cryo_Necro_State = wizardFight(attacker, defender, location, Cryo_Necro_State)
   geoDf = geoDf.append({"attacker":attacker, "defender":defender, "location":location, "victor":victor}, ignore_index=True)
  if location=="Cryo":
   defender=random.choice(Cryomancers)
   victor, Cryo_Necro_State = wizardFight(attacker, defender, location, Cryo_Necro_State)
   cryoDf = cryoDf.append({"attacker":attacker, "defender":defender, "location":location, "victor":victor}, ignore_index=True)
  #Oh and also there's a war on now
  random.shuffle(Vitamancers)
  random.shuffle(Pyromancers)
  if random.choice([True, False]) or r==503: #Do pyros get to go first? And/or is it the turn during which the Pyros launched their sneak attack?
   location="Vita"
   for matchup in [0,1]:
    attacker=Pyromancers[matchup]
    defender=Vitamancers[matchup]
    victor, Cryo_Necro_State = wizardFight(attacker, defender, location, Cryo_Necro_State)
    vitaDf = vitaDf.append({"attacker":attacker, "defender":defender, "location":location, "victor":victor}, ignore_index=True)
  else:
   location="Pyro"
   for matchup in [0,1]:
    attacker=Vitamancers[matchup]
    defender=Pyromancers[matchup]
    victor, Cryo_Necro_State = wizardFight(attacker, defender, location, Cryo_Necro_State)
    vitaDf = vitaDf.append({"attacker":attacker, "defender":defender, "location":location, "victor":victor}, ignore_index=True)
 #Necros attack!
 elif r<1111:
  goodies=Vitamancers+Geomancers
  baddies=Necromancers+Pyromancers
  random.shuffle(goodies)
  random.shuffle(baddies)
  goodieAttackLocations=["Necro","Pyro","Pyro"]
  baddieAttackLocations=["Vita","Vita","Vita","Geo","Geo"]
  for i in range(len(goodies)):
   if random.choice([True, False]) or r==954: #Do baddies get to go first? And/or is it the turn Necros joining in left everyone scrambling?
    attacker=baddies[i]
    defender=goodies[i]
    location=random.choice(baddieAttackLocations)
    victor, Cryo_Necro_State = wizardFight(attacker, defender, location, Cryo_Necro_State)
    geoDf = geoDf.append({"attacker":attacker, "defender":defender, "location":location, "victor":victor}, ignore_index=True)
   else:
    attacker=goodies[i]
    defender=baddies[i]
    location=random.choice(goodieAttackLocations)
    victor, Cryo_Necro_State = wizardFight(attacker, defender, location, Cryo_Necro_State)
    geoDf = geoDf.append({"attacker":attacker, "defender":defender, "location":location, "victor":victor}, ignore_index=True)
 else:
  goodies=Vitamancers+Geomancers+Cryomancers
  baddies=Necromancers+Pyromancers
  random.shuffle(goodies)
  random.shuffle(baddies)
  goodieAttackLocations=["Necro","Pyro","Pyro"]
  baddieAttackLocations=["Vita","Geo", "Cryo"]
  for i in range(len(goodies)):
   if random.choice([True, False]) or r==954: #Do baddies get to go first? And/or is it the turn Necros joining in left everyone scrambling?
    attacker=baddies[i]
    defender=goodies[i]
    location=random.choice(baddieAttackLocations)
    victor, Cryo_Necro_State = wizardFight(attacker, defender, location, Cryo_Necro_State)
    geoDf = geoDf.append({"attacker":attacker, "defender":defender, "location":location, "victor":victor}, ignore_index=True)
   else:
    attacker=goodies[i]
    defender=baddies[i]
    location=random.choice(goodieAttackLocations)
    victor, Cryo_Necro_State = wizardFight(attacker, defender, location, Cryo_Necro_State)
    geoDf = geoDf.append({"attacker":attacker, "defender":defender, "location":location, "victor":victor}, ignore_index=True)
 if r==954:
  geoDf=geoDf.append(vitaDf) #Vitas share info
 if r==1111:
  geoDf=geoDf.append(cryoDf) #Cryos share info
  

def remancer(txt):
 parts = txt.split(" ")
 if len(parts)==1:
  return txt+"mancer"
 else:
  return parts[0]+"mancer "+parts[1]

print(remancer("Necro A"))


geoDf["location"]=geoDf["location"]+"mancer Territory"
geoDf["attacker"]=geoDf["attacker"].apply(remancer)
geoDf["defender"]=geoDf["defender"].apply(remancer)
geoDf["victor"]=geoDf["victor"].apply(remancer)

print(geoDf)

print(wizardOdds("Cryo", "Necro A", "Pyro", Cryo_Necro_State))

geoDf.to_csv("dset.csv")
