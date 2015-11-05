#!/usr/bin/python3

import sys
import fileinput
import os.path
import json
from collections import namedtuple
import string
import re

def is_ascii(text):
	# Returns true if text does not contain any non-ascii characters
	return all(ord(c) < 128 for c in text)

def clean_text(text):
	# Returns a tuple containing two values
	# The first one is a boolean value to indicate if text contained non-ascii characters
	# The second is a cleaned string without any non-ascii characters and escaped whitespace characters
	text = re.sub(r"[\s]", ' ', text)
	u = False
	Result = namedtuple ('Result', 'unicode text')
	if not is_ascii(text):
		u = True
	ctext = ''.join(filter(lambda x: x in string.printable, text))
	return Result(u, ctext)

# First function to be executed
def main():
	# Reads input file and writes feauture 1 into output file as specified in cmd arguments
	if(os.path.isfile(sys.argv[1])):
		ipfile = open(sys.argv[1], "r")
	else:
		# Terminates if input file path is invalid
		print("Invalid input path: ", sys.argv[1])
		exit(0)
	opfile = open(sys.argv[2], "w+")
	count = 0
	s = ""
	print("Creating feature file 1: ", sys.argv[2])
	for line in ipfile:
		parsed_json = json.loads(line)
		if "text" and "created_at" in parsed_json:
			text = parsed_json["text"]
			timestamp = parsed_json["created_at"]
			result = clean_text(text)
			s += result.text + " (timestamp: " + timestamp +")\n"
			if result.unicode:
				count += 1
	s += "\n" + str(count) + " tweets contained unicode."
	opfile.write(s)
	ipfile.close()
	opfile.close()

# Execution starts here
main()	
