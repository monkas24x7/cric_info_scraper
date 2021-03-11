from datascrp import Player
import json
from tqdm import tqdm
with open("player_ids.json","r") as infile:
	ids=json.load(infile)
dic={}
# for x in tqdm(ids.keys()):
# 	for xx in ids[x]:
plyr=Player(35320)
dic[plyr._name()]={}
fields=dic[plyr._name()]
fields["name"]=plyr._name()
fields["full_name"]=plyr._full_name()
fields["date_of_birth"]=plyr._date_of_birth()
fields["country"]="India"
fields["photo"]=plyr.photo()
fields["major_teams"]=plyr._major_teams()
fields["role"]=plyr._playing_role()["name"]
col1=plyr._batting_style()
if col1!=None:
	fields["batting_style"]=col1["description"]
else:
	fields["batting_style"]=None
col2=plyr._bowling_style()
if col2!=None:
	fields["bowling_style"]=col2["description"]
else:
	fields["bowling_style"]=None
fields["bat_avg"]=plyr._batting_fielding_averages()
fields["bowl_avg"]=plyr._bowling_averages()
fields["test_debut"]=plyr._test_debut()
fields["last_test"]=plyr._last_test()
fields["odi_debut"]=plyr._odi_debut()
fields["last_odi"]=plyr._last_odi()
fields["t20i_debut"]=plyr._t20i_debut()
fields["last_t20i"]=plyr._last_t20i()
fields["first_class_debut"]=plyr._first_class_debut()
fields["last_first_class"]=plyr._last_first_class()
fields["list_a_debut"]=plyr._list_a_debut()
fields["last_list_a"]=plyr._last_list_a()
fields["t20_debut"]=plyr._t20_debut()
fields["last_t20"]=plyr._last_t20()
# with open("player_data_all.json","r") as outfile:
# 	json.dump(dic,outfile,indent=3)
print(json.dumps(dic, indent=3))

