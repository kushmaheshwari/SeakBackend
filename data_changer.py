from urlparse import urlparse
import httplib2 as http
import json
import time


def main():


	with open("/Users/kushmaheshwari/Documents/development/SeakBackend/first50.txt", "r") as ins:
		with open('/Users/kushmaheshwari/Documents/development/SeakBackend/first50changed.txt', 'w') as outfile:

			for line in ins:

				line = changeline(line)
				outfile.write(line + "\n")

	teststring = "Belkin Sport-Fit Armband For Galaxy S6/S6 Edge - Black,745883676057,24.99"
	changeline(teststring)

	# categoryDict = {}

	# categoryDict["Wires"] = ["chargers","cables","usb","extensions","wires","wire","extension","cable","aux","micro-usb","micro usb","charge","ft",
	# 						"in","inch","feet","power cord"]

	# categoryDict["Case"] = ["ottobox","box","case","cover","full body","snapfit","elastic fit","case-mate","evutec","dog and bone","ghostek","griffin"
	# 						,"incipio","hardshell","softshell","gel","lifeproof","lunatik","magpul","otterbox","spigen","armour","armor"]

	# categoryDict["Headphones"] = ["headphones", "earphones", "over-ear", "in-ear", "over ear", "in ear", "headset","handsfree","in ear","skullcandy"]

	# categoryDict["Screen protectors"] = ["plastic screen cover", "shatter proof screen cover", "shatter-proof","screen protector","screen cleaner",
	# 									"microfiber","safegaurd"]

	# categoryDict["Accessories"] = ["armband","battery","adapter","charger","speaker","bluetooth","holder","stylus","pen","mount"]


	# string = "Belkin Sport Fit Armband For iPhone 5/5c/5s/SE - Blacktop And Overcast"

	# key = getCategory(string, categoryDict)

	# print key


def getCategory(title, categoryDict):
	# global categoryDict

	titlelowercase = title.lower()
	titlesplit = titlelowercase.split(" ")
	for key in categoryDict:
		options = categoryDict[key]
		for option in options:
			if(option in titlesplit):
				print option
				return key

	return None




def changeline(line):
	s = list(line)

	for i in range(0,len(s)):
		if s[i] == "-" and s[i+1] != " " and s[i-1] != " ":
			s[i] = " "

	return "".join(s).rstrip()





if __name__ == '__main__':
    main()



