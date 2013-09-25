#!/usr/bin/env python


from sys import argv
from parseme import identify_type
from pprint import pprint

def main():

	with open(argv[1], "r") as f:
	    lines = f.readlines()

	course_exceptions = []
	for line in lines:
		line = line.rstrip()
		print identify_type(line) + "|-->>  " + line
		# if identify_type(line) == "UNSURE":
		# 	course_exceptions.append(line)

	# pprint(list(set(course_exceptions)))

if __name__ == '__main__':
	main()