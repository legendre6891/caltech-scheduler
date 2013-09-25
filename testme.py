#!/usr/bin/env python


from sys import argv
from parseme import identify_type


def main():

	with open(argv[1], "r") as f:
	    lines = f.readlines()

	for line in lines:
		line = line.rstrip()
		print identify_type(line) + "|-->>  " + line

if __name__ == '__main__':
	main()