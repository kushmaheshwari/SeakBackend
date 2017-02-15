from urlparse import urlparse
import httplib2 as http
import json

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}




ch = http.Http()
categoryDict = makeCategoryDictionary()
base_url = 'https://api.upcitemdb.com/prod/trial/lookup?upc='


with open("/Users/kushmaheshwari/Documents/development/upc_codes", "r") as ins:
	for line in ins:
		data = getItemInfo(line)
		
		items = data["items"]
		itemsDict = items[0]

		print "Title: " + itemsDict["title"]

		category = getCategories(itemsDict["title"])

		print "Category: " + category

		print "Description: " + itemsDict["description"]
		print "Color: " + itemsDict["color"]

		images = itemsDict["images"]
		print "Image url: " + images[0]

		print "\n"



def getCategories(title):
	for key in categoryDict:
		options = categoryDict[key]
		for option in option:
			titlelowercase = title.lower()
			if(option in titlelowercase):
				return key

	return None

def getItemInfo(line):
	url = base_url + line
	url = url.strip()
	lookup = urlparse(url)
	resp, content = ch.request(lookup.geturl(), 'GET', '', headers)
	data = json.loads(content)
	return data

def makeCategoryDictionary():
	categoryDict = {}
	categoryDict["Wires"] = ["chargers","cables","usb","extensions","wires","wire","extension","cable"]
	categoryDict["Case"] = ["ottobox","box","case","cover","full body","snapfit","elastic fit"]
	categoryDict["Headphones"] = ["Headphones", "earphones", "over-ear", "in-ear", "over ear", "in ear", "headset"]
	categoryDict["Screen protectors"] = ["plastic screen cover", "shatter proof screen cover", "shatter-proof"]

	return categoryDict


Wires: Chargers, cables, USB, extensions, wires, wire, extension, cable
Case: Ottobox, box, case, cover, full body, snapfit, elastic fit
Headphones: Headphones, earphones, over-ear, in-ear, over ear, in ear, headset
Screen protectors: Plastic screen cover, shatter proof screen cover, shatter-proof
Services *MANUALLY ENTERED*











