from urlparse import urlparse
import httplib2 as http
import json
import time

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

ch = http.Http()
base_url = 'https://api.upcitemdb.com/prod/trial/lookup?upc='

ordering = {'title': 0, 'description': 1, 'price': 2, 'category': 3}


def main():

	
	global categoryDict
	categoryDict = makeCategoryDictionary()
	
	previoustitle = None
	previousdict = None
	previousPrice = -1


	with open("/Users/kushmaheshwari/Documents/development/SeakBackend/testupc.txt", "r") as ins:
		with open('/Users/kushmaheshwari/Documents/development/SeakBackend/output.txt', 'a') as outfile:
    
			for line in ins:

				time.sleep(20)

				#split line by comma and dash (remove whitespace for both)
				line_split_comma = splitLineComma(line)
				title_split_dash = splitTitleDash(line_split_comma[0])
				newdict = None

				if((title_split_dash[0] == previoustitle) and (len(title_split_dash) == 2) and (float(line_split_comma[2]) == previousPrice)):					#same item different color; single dash
					print "here"
					newdict = addTypeExistingDictSingleDash(previousdict,line_split_comma,title_split_dash)

				elif((title_split_dash[0] == previoustitle) and (len(title_split_dash) == 3) and (float(line_split_comma[2]) == previousPrice)):				#same item different color; double dash
					newdict = addTypeExistingDictDoubleDash(previousdict,line_split_comma,title_split_dash)


				else:

					json.dump(previousdict,outfile,indent = 4)
					outfile.flush()

					outfile.write("\n\n")
																										# new item
					if(len(title_split_dash) == 1): 																#One type
						newdict = makeSingleType(line, line_split_comma,title_split_dash)

					elif(len(title_split_dash) == 2):																# multiple types
						newdict = makeMultipleTypeSingleDash(line, line_split_comma,title_split_dash)

					else: 																					# multiple types with extra dash
						newdict = makeMultipleTypeTwoDash(line, line_split_comma,title_split_dash)


				previoustitle = title_split_dash[0]
				previousdict = newdict
				previousPrice = float(line_split_comma[2].rstrip())

			json.dump(previousdict,outfile,indent = 4)



def addTypeExistingDictSingleDash(previousdict, line_split_comma, title_split_dash):
	data = getItemInfo(line_split_comma[1])
	items = data["items"]
	if len(items) > 0:
		itemsDict = items[0]
		images = itemsDict["images"]

		typelist = previousdict["types"]

		type_json = {}
		type_json["color"] = title_split_dash[1]
		if len(images) > 0:
			type_json["imageurl"] = images[0]
		else:
			type_json["imageurl"] = ""
		type_json["upc"] = line_split_comma[1]

		typelist.append(type_json)

		previousdict["types"] = typelist

		return previousdict

def addTypeExistingDictDoubleDash(previousdict, line_split_comma, title_split_dash):
	data = getItemInfo(line_split_comma[1])
	print data
	items = data["items"]
	itemsDict = items[0]
	images = itemsDict["images"]

	typelist = previousdict["types"]

	type_json = {}
	type_json["color"] = title_split_dash[2]
	if len(images) > 0:
		type_json["imageurl"] = images[0]
	else:
		type_json["imageurl"] = ""
	type_json["upc"] = line_split_comma[1]

	typelist.append(type_json)

	previousdict["types"] = typelist

	return previousdict

#combine above 2 functions

def makeMultipleTypeTwoDash(line, line_split_comma,title_split_dash):
	data = getItemInfo(line)
	items = data["items"]
	itemsDict = items[0]

	line_split_comma = line.split(",")

	item_dict = {}

	item_dict["title"] = title_split_dash[0] + " - " + title_split_dash[1]
	item_dict["description"] = itemsDict["description"]
	item_dict["price"] = float(line_split_comma[2].rstrip())
	item_dict["category"] = getCategory(title_split_dash[0])

	images = itemsDict["images"]
	type_json = {}
	type_json["color"] = title_split_dash[1]
	if len(images) > 0:
		type_json["imageurl"] = images[0]
	else:
		type_json["imageurl"] = ""
	type_json["upc"] = line_split_comma[1]

	typelist = []
	typelist.append(type_json)
	item_dict["types"] = typelist

	return item_dict


def makeMultipleTypeSingleDash(line, line_split_comma,title_split_dash):
	data = getItemInfo(line_split_comma[1])
	# print line
	# print data
	if("items" not in data):
		print line
		print data
	items = data["items"]
	itemsDict = items[0]

	line_split_comma = line.split(",")

	item_dict = {}

	item_dict["title"] = title_split_dash[0]
	item_dict["description"] = itemsDict["description"]
	item_dict["price"] = float(line_split_comma[2].rstrip())
	item_dict["category"] = getCategory(line_split_comma[0])

	images = itemsDict["images"]
	type_json = {}
	type_json["color"] = title_split_dash[1]
	if len(images) > 0:
		type_json["imageurl"] = images[0]
	else:
		type_json["imageurl"] = ""
	type_json["upc"] = line_split_comma[1]

	typelist = []
	typelist.append(type_json)
	item_dict["types"] = typelist

	return item_dict

def makeSingleType(line, line_split_comma,title_split_dash):
	data = getItemInfo(line_split_comma[1])
	items = data["items"]
	itemsDict = items[0]

	line_split_comma = line.split(",")

	item_dict = {}

	item_dict["title"] = title_split_dash[0]
	item_dict["description"] = itemsDict["description"]
	item_dict["price"] = float(line_split_comma[2].rstrip())
	item_dict["category"] = getCategory(line_split_comma[0])

	images = itemsDict["images"]
	type_json = {}
	if len(images) > 0:
		type_json["imageurl"] = images[0]
	else:
		type_json["imageurl"] = ""
	type_json["upc"] = line_split_comma[1]

	typelist = []
	typelist.append(type_json)
	item_dict["types"] = typelist

	return item_dict



def getItemInfo(line):
	url = base_url + line
	url = url.strip()
	lookup = urlparse(url)
	resp, content = ch.request(lookup.geturl(), 'GET', '', headers)
	data = json.loads(content)
	return data

def getCategory(title):
	global categoryDict
	titlelowercase = title.lower()
	titlesplit = titlelowercase.split(" ")
	for key in categoryDict:
		options = categoryDict[key]
		for option in options:
			if(option in titlesplit):
				return key

	return None



def splitLineComma(line):
	line_split_comma = line.split(",")
	for i in range(len(line_split_comma)):
		item = line_split_comma[i]
		item = item.strip()
		line_split_comma[i] = item

	return line_split_comma

def splitTitleDash(title):
	title_split_dash = title.split("-")
	for i in range(len(title_split_dash)):
		item = title_split_dash[i]
		item = item.strip()
		title_split_dash[i] = item

	return title_split_dash

def makeCategoryDictionary(): #search for wire before cable
	categoryDict = {}

	categoryDict["Wires"] = ["chargers","cables","usb","extensions","wires","wire","extension","cable","aux","micro-usb","micro usb","charge","ft",
							"in","inch","feet","power cord"]

	categoryDict["Case"] = ["ottobox","box","case","cover","full body","snapfit","elastic fit","case-mate","evutec","dog and bone","ghostek","griffin"
							,"incipio","hardshell","softshell","gel","lifeproof","lunatik","magpul","otterbox","spigen","armour","armor"]

	categoryDict["Headphones"] = ["headphones", "earphones", "over-ear", "in-ear", "over ear", "in ear", "headset","handsfree","in ear","skullcandy"]

	categoryDict["Screen protectors"] = ["plastic screen cover", "shatter proof screen cover", "shatter-proof","screen protector","screen cleaner",
										"microfiber","safegaurd"]

	categoryDict["Accessories"] = ["armband","battery","adapter","charger","speaker","bluetooth","holder","stylus","pen","mount"]

	return categoryDict




if __name__ == '__main__':
    main()


