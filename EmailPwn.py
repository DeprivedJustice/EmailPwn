#!/usr/bin/python3
import requests
import sys
from pyvirtualdisplay import Display
from selenium import webdriver
import json
import pandas as pa
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class info:
	def __init__(self,query,lookuptype):
		self.query = query
		self.lookuptype = lookuptype.lower()
		self.apikey = "230d5357faf1155187111d8236a4204d324d5398"
		self.emailrepkey = "kanmzsmlkhwfcw5nge0f4z64dxgr3dj3btho9bimqw8g2bak"
	def parsebreach(self,data):
		ndata = data.replace("{'success': True, 'found': ","").replace(", 'result': [{'line': '","").replace(", {'line': '","").replace("{","").replace("}","").replace("]","").replace("'","\n").replace(", u","").replace("line","").replace(": u","").replace(": [u","").replace("result","").replace("success","").replace(": True","").replace("found","")
		return ndata
	def stripdata(self,data):
		ndata = data.replace('"result":[{"line":"',"").replace('"',"").replace("{","").replace("}","").replace("]","").replace("[","").replace("line:","")
		return ndata
	def lookup(self):
		if(self.lookuptype == "email"):
			self.checkbreaches()
			self.checkemailrep()
		elif(self.lookuptype == "ip"):
			self.iptoaddr()
			return


		req = requests.post(f"https://leakcheck.net/api/?key={self.apikey}&check={self.query}&type={self.lookuptype}")
		if("false" in req.text):
			print(f"No Results Found for '{self.query}'")
			return

		userandpasswords = []
		self.passwords = []
		get = req.text.split(",")
		for g in get:
			new = self.stripdata(g)
			self.passwords.append(new)
	def checkbreaches(self):
		self.breaches = []
		display = Display(visible=0, size=(800, 600))
		display.start()
		b = webdriver.Firefox()
		try:
			
			b.get('https://haveibeenpwned.com/unifiedsearch/'+self.query)
		
			lol = b.find_elements_by_xpath("//html")
			for t in lol:
				info = t.text
	
				p = self.parsebreach(info.replace('"',"").replace("[","").replace("Breaches:","").replace("Names",""))
				l = p.split(",")
				for line in l:
					if("Name" in line):
						self.breaches.append(line.replace("Name","").replace(":",""))
					else:
						pass
			b.quit()
			display.stop()
			os.system("rm -rf geckodriver.log")
		except:
			os.system("rm -rf geckodriver.log")

	def checkemailrep(self):
		headers = {
			"Key":self.emailrepkey,
			"User-Agent":"Tor" #yiyi
		}
		r = requests.get("https://emailrep.io/{self.query}",headers=headers)
		self.emailrep = r.text.replace(" ","").replace("\n","").strip('":"{,}').replace('"',"").replace("}","").replace("[","").replace("]","").replace("{","").split(",")
		
	def iptoaddr(self):
		b = webdriver.Chromium()
		b.get("https://thatsthem.com/ip/{self.query}")

		tmp = b.page_source.split(">")

		for line in tmp:
			if('<span itemprop="telephone">' in line):
				print(line)

		
	def results(self):
		print("NOTE: there is no order, just because the data is next to the breach dosent mean that password will work for that website")
		del self.passwords[0]
		del self.passwords[0]
		passwords = pa.Series(self.passwords)


		if(self.lookuptype == "email"):
			breaches = pa.Series(self.breaches)
			rep = pa.Series(self.emailrep)
			data = {'DATA':  passwords ,
					'BREACHES':breaches.reindex(passwords.index),
					'EMAIL-REP':rep.reindex(passwords.index)
	        }
			df = pa.DataFrame (data, columns = ['DATA',"BREACHES","EMAIL-REP"])
		else:
			data = {'DATA':  passwords 
	        }
			df = pa.DataFrame (data, columns = ['DATA'])

		pa.set_option('display.max_rows', df.shape[0]+1)


		print(df)




#username = login
#email = email
#keyword = mass
if(len(sys.argv) < 3):
	print(f"python {sys.argv[0]} [searchquery] [email|login|mass]")
else:
	query = sys.argv[1]
	stype = sys.argv[2]

	l = info(query,stype)
	l.lookup()
	#l.results()
