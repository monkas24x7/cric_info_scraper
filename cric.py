import re
import json
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.request import urlopen
url="https://www.espncricinfo.com/ci/content/player/index.html?country=6"
page=urlopen(url)
html=page.read().decode("utf-8")
soup= str(BeautifulSoup(html, "html.parser"))
reg1='<a href="index\\.html\\?country=(\\d+)">([\\w ]*)<\\/a>'
reg2='<option value="([\\d]*)">([\\w ]*)<\\/option>'
m1=re.findall(reg1,soup)
m1=m1+re.findall(reg2,soup)
teamcodes={}
for x in m1:
	teamcodes[x[1]]=x[0]
dic={}
for xx in tqdm(teamcodes.keys()):
	dic[xx]=[]
	for xxx in range(65,91):
		url=f'https://www.espncricinfo.com/ci/content/player/country.html?country={teamcodes[xx]};alpha={chr(xxx)}'
		page=urlopen(url)
		html=page.read().decode("utf-8")
		soup= str(BeautifulSoup(html, "html.parser"))
		reg3='href="\\/ci\\/content\\/player\\/([\\d]+)\\.html"'
		dic[xx]+=re.findall(reg3,soup)
with open("player_ids.json","w") as outfile:
	json.dump(dic,outfile, indent=4)





