#!/usr/bin/env python


import re
from sys import argv

def enum(**enums):
    return type('Enum', (), enums)


def word_number_split(word):
	match = re.match(r"([a-z]+)([0-9]+[A-Z]*$)", word, re.I)
	if match:
		items = match.groups()
	else:
		items = [word]

	return list(items)

def is_course_word(word):
	if re.match("^[A-Za-z,-]*$", word):
		return True
	else:
		return False


def flatten_level_one_list(xs):
	return [a for b in xs for a in b]

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_sublist_of(xs, ys):
	# tests if xs is a sublist of ys
	return all([x in ys for x in xs])



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
	return token[-2][-1] == ',' and token[-1].isupper() and len(token[-1]) == 1

def is_day_time(token, string):

	# first test whether token[0] is a date abbreviation;
	allowed_abbreviations = "MTWRF"
	allowed_words = ["OM"]

	is_abbreviated = lambda word: all([ch in allowed_abbreviations for ch in word])
	is_allowed = lambda word: word in allowed_words
	pass_function = lambda word: is_allowed(word) or is_abbreviated(word)


	tokenpass = [0, 0, 0, 0]
	tokenpass[0] = all([pass_function(word) for word in token[0].split(',')])

	# now test for the other four tokens
	is_time = lambda string: all([is_int(part) for part in string.split(':')]) \
		and	len(string.split(':')) == 2

	tokenpass[1] = is_time(token[1])
	tokenpass[3] = is_time(token[3])

	tokenpass[2] = token[2] == '-'
	return all(tokenpass)

def is_location(token, string):
	manual_locations = ["House STL",
	 "YHC",
	 "BRW",
	 "BAC",
	 "MPR BAC",
	 "SOF BAC",
	 "POOL BAC",
	 "TCT BAC",
	 "BAC",
	 "NOF BAC",
	 "MEAD",
	 "TRK BAC",
	 "TCT",
	 "Garage TCT",
	 "Library AVE",
	 "L+R"]
	manual_buildings = ["L+R"]
	manual_locations_tokens = [initial_parse(location)[0] \
		for location in manual_locations]

	location_override = lambda token: token in manual_locations_tokens

	all_caps = lambda word: all([ch.isupper() for ch in word])
	building_pass = lambda building: all_caps(building) or \
		building in manual_buildings

	location_pattern = lambda token: is_int(token[0]) and \
		building_pass(token[1]) and \
		len(token) == 2

	return location_override(token) or location_pattern(token)

def is_grade_scheme(token, string):
	schemes = ["PASS-FAIL", "LETTER"]
	return token in [initial_parse(s)[0] for s in schemes]

def is_A(token, string):
	A = ["A"]
	return token in [initial_parse(s)[0] for s in A]

def is_location_part(token, string):
	parts = ["Auditorium",
	"BRD",
	"Lecture Hall",
	"BAX",
	"Institute",
	"Auditorium",
	"BCK",
	"Basement",
	"Ramo",
	"BAX",
	"Ceramic",
	"Room POLY"]

	return token in [initial_parse(s)[0] for s in parts]

def is_annotation(token, string):
	annotations = ["taught",
		"updated",
		"lottery",
		"change in",
		"Permission",
		"graduate students only",
		"enrollment",
		"Make-up",
		"cancelled",
		"Most sessions",
		"session",
		"research advisor",
		"Required",
		"Taught",
		"Prerequisite",
		"lecture time",
		"Lecture Recitation Tutorial",
		"permission",
		"offered",
		"arrangement",
		"Field Trip",
		"updated",
		"Sec",
		"Formerly",
		"Section",
		"will meet"
	]
	tokenized_annotations = [initial_parse(ann)[0] for ann in annotations]

	return any([is_sublist_of(tok_ann, token) for tok_ann in tokenized_annotations])

def is_time_part(token, string):
	is_time = lambda string: all([is_int(part) for part in string.split(':')]) \
		and	len(string.split(':')) == 2
	return is_time(token[0])

def is_course_title(token, string):
	return all([is_course_word(tok) for tok in token])

def is_unsure(token, string):
	return True

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
	(lambda t, s: [filter(lambda word: len(word) > 0, t), s], 6)
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

LINE_TYPES = {"COURSE_NAME" : [is_course_name],
				  "UNITS" : [is_units],
				  "SECTION" : [is_section],
				  "PROFESSOR_NAME" : [is_professor_name],
				  "DAY_TIME" : [is_day_time],
				  "LOCATION" : [is_location],
				  "GRADE_SCHEME" : [is_grade_scheme],
				  "A" : [is_A],
				  "LOCATION_PART" : [is_location_part],
				  "ANNOTATION" : [is_annotation],
				  "TIME_PART" : [is_time_part],
				  "COURSE_TITLE" : [is_course_title]}


def identify_type(line):

	type_list = []

	[token, string] = initial_parse(line)
	for line_type, line_test in LINE_TYPES.iteritems():
		if line_test[0](token, string) == True:
			type_list.append(line_type)

	if type_list == []:
		return "UNSURE"
	else:
		return ' '.join(type_list)

def main():
	print initial_parse(argv[1])



if __name__ == '__main__':
	main()