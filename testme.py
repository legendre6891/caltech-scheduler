#!/usr/bin/env python


from sys import argv
from parseme import *


def main():
	print initial_parse(argv[1])

	with open(argv[1], "r") as f:
	    lines = f.readlines()

	for line in lines:
		print identify_type(line), line

if __name__ == '__main__':
	main()