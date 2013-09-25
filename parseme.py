#!/usr/bin/env python


import re
from sys import argv


def word_number_split(word):
	match = re.match(r"([a-z]+)([0-9]+[A-Z]*$)", word, re.I)
	if match:
		items = match.groups()
	else:
		items = [word]

	return list(items)

def flatten_level_one_list(xs):
	return [a for b in xs for a in b]

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_course_name(token, string):
	options = ['Ae', 'An', 'ACM', 'AM', 'APh', 'Art', 'Ay', 'BMB', 'BE', 'Bi',
	'BEM', 'Ch', 'CHE', 'CDS', 'CNS', 'CS', 'CE', 'Ec', 'ESL', 'EE', 'E', 'EN',
	'ESE', 'F', 'FS', 'Ge', 'H', 'HPS', 'Hum', 'L', 'Law', 'Ma', 'MS', 'ME',
	'Mu', 'Pl', 'PE', 'Ph', 'PS', 'PA', 'Psy', 'SS', 'SA', 'Wr']
	return token[0] in options

def is_units(token, string):
	s = string.split('-')
	return string == '+' or (len(s)==3 and all(map(is_int, s)))

def is_section(token, string):
	return is_int(string)


def is_professor_name(token, string):
	return token[-2][-1] == ',' and token[-1].isupper()

def is_day_time(token, string):

	# first test whether token[0] is a date abbreviation;
	allowed_abbreviations = "MTWRF"
	allowed_words = ["OM"]

	is_abbreviated = lambda word: all([ch in allowed_abbreviations for ch in word])
	is_allowed = lambda word: word in allowed_words
	pass_function = lambda word: is_allowed(word) or is_abbreviated(word)

	token_zero_pass = all([pass_function(word) for word in token[0].split(',')])
	return token_zero_pass

def initial_parse(current_line):

	# In the current implementation, this is the *first*
	# function that is performed on current_line.
	# zero_parse: string -> [strings]
	zero_parse = lambda s: s.split(' ')


	# initial_parse_functions is a list of (func, priority)
	# where:
	#
	# func `f' have the signature:
	# f: [[strings], string] -> [[strings], string]
	#
	# priority is a number.
	initial_parse_functions = [
	(lambda t, s: [map(word_number_split, t),s], 2),
	(lambda t, s: [flatten_level_one_list(t), s], 3),
	(lambda t, s: [map(lambda string: string.split('/'), t), s], 4),
	(lambda t, s: [flatten_level_one_list(t), s], 5),
	]

	# Each of the func's in initial_parse_functions is run on [token, string]
	# in order of increasing priority (1 is run first!)
	# the input to the first is: [token, current_line]
	initial_parse_functions = sorted(initial_parse_functions, key=lambda l: l[1])

	token = zero_parse(current_line)
	string = current_line
	for (function, priority) in initial_parse_functions:
		[token, string] = function(token, string)


	return [token, string]



def main():
	print initial_parse(argv[1])



if __name__ == '__main__':
	main()