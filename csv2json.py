#!/usr/bin/python
#
# csv2json.py
#
# posterestante - 4 May 2016
#
# Description: Quick 'n dirty script to render a specifically structured CSV in HTML-friendly JSON - either updating an existing JSON file or creating a new one
# Usage: ./csv2json.py /path/to/input /path/to/output
#
# Note: CSV must be encoded as Windows-1252 (default 'Windows CSV' output from Microsoft Excel)
# Note: JSON file (if present) must be encoded as UTF-8
#

import sys
import errno
import codecs
import csv
import json

# Clean up input from Excel, including converting from Windows-1252 to ASCII encoding with HTML special characters and changing carriage returns to line breaks and removing tabs
def cleaninput(input = []):
	cleaned = []
	for row in input:
		cleanedrow = []
		for item in row:
			item = item.decode('cp1252').encode('ascii', 'xmlcharrefreplace')
			item = item.replace("\r", "\n")
			item = item.replace("\t", "")
			cleanedrow.append(item)
		cleaned.append(cleanedrow)
	return cleaned

# Use 'hash' column in the data to match existing JSON entries with values from the CSV file, update them according to the CSV if matched and adding them as new entries if not
def updatejson(csvrows = [], jsonrows = []):
	newentries = []
	for csvrow in csvrows:
		matched = False
		for jsonrow in jsonrows:
			if jsonrow["hash"] == csvrow[0]:
				matched = True
				print "Matched", csvrow[1]
				jsonrow["name"] = csvrow[1]
				jsonrow["position"] = csvrow[2]
				jsonrow["organisation"] = csvrow[3]
				jsonrow["title"] = csvrow[7]
				jsonrow["statement"] = csvrow[8]
				jsonrow["teaser"] = csvrow[9]
				jsonrow["bio"] = csvrow[10]
				jsonrow["tags"] = csvrow[11]
				jsonrow["location"] = csvrow[12]
				jsonrow["profile"] = csvrow[13]
				jsonrow["url"] = csvrow[14]
				jsonrow["twitter"] = csvrow[16]
				jsonrow["tweet"] = csvrow[17]
		if matched == False:
			newentries.append(json.dumps( { "hash": csvrow[0], "name": csvrow[1], "position": csvrow[2], "organisation": csvrow[3], "title": csvrow[7], "statement": csvrow[8], "teaser": csvrow[9], "bio": csvrow[10], "tags": csvrow[11], "location": csvrow[12], "profile": csvrow[13], "url": csvrow[14], "twitter": csvrow[16], "tweet": csvrow[17] }, sort_keys=True, indent=4))
	return "[" + json.dumps(jsonrows, sort_keys=True, indent=4).replace("[", "").replace("]", "") + "," + ",".join(newentries) + "]"

# Render all new JSON entries with values from the CSV file
def newjson(csvrow = []):
	jsonrows = []
	jsonrows.append("[")
	for row in csvrows:
		jsonrows.append(json.dumps( { "hash": row[0], "name": row[1], "position": row[2], "organisation": row[3], "title": row[7], "statement": row[8], "teaser": row[9], "bio": row[10], "tags": row[11], "location": row[12], "profile": row[13], "url": row[14], "twitter": row[16], "tweet": row[17] }, sort_keys=True, indent=4))
	jsonrows.append("]")
	return jsonrows

# Chek CLI arguments
if len(sys.argv) != 3:
	print "Usage: ./csv2json.py /path/to/input /path/to/output"
	print "Note: Save the Manifesto XLSX to XLS, then to Windows CSV to get the appropriate encoding"
	print "Note: requires specific column structure - do not add or remove columns in the Excel sheet"
	sys.exit()

# Initialise lists
csvrows = []
jsonrows = []

# Read the CSV
try:
	sourcefile = open(sys.argv[1], 'r',)
	csvreader = csv.reader(sourcefile)
	csvrows = cleaninput(csvreader)
	sourcefile.close()
except IOError:
	print "Cannot open", sys.argv[1]
	sys.exit()
except:
	print "Error parsing CSV in", sys.argv[1]
	sys.exit()

# Check if JSON exists, set output
try:
	destinationfile = codecs.open(sys.argv[2], 'r', encoding='utf-8')
	jsonreader = json.load(destinationfile)
	for row in jsonreader:
		jsonrows.append(row)
	destinationfile.close()
	output = updatejson(csvrows, jsonrows)
except IOError as e:
	if e.errno != errno.ENOENT:
		print "Cannot open", sys.argv[2]
		sys.exit()
	output = newjson(csvrows)
except:
	print "Error parsing JSON in", sys.argv[2]
	sys.exit()

# Write output as JSON to file
try:
	destinationfile = codecs.open(sys.argv[2], 'w', encoding='utf-8')
	for row in output:
		destinationfile.write(row)
	destinationfile.close()
except IOError:
	print "Cannot write to", sys.argv[2]
	sys.exit()

print "Update successful!"
