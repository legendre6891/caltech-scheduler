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
	if re.match("^[A-Za-z,\-]*$", word):
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

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



def is_sublist_of(xs, ys):
	# tests if xs is a sublist of ys
	return all([x in ys for x in xs])

def is_day_abbreviation(words):
	# first test whether token[0] is a date abbreviation;
	allowed_abbreviations = "MTWRFS"
	allowed_words = ["OM", "OM,A"]

	is_abbreviated = lambda word: all([ch in allowed_abbreviations for ch in word])
	is_allowed = lambda word: word in allowed_words
	pass_function = lambda word: is_allowed(word) or is_abbreviated(word)


	return all([pass_function(word) for word in words.split(',')])


def is_course_name(token, string):
	options = ['Ae', 'An', 'ACM', 'AM', 'APh', 'Art', 'Ay', 'BMB', 'BE', 'Bi',
	'BEM', 'Ch', 'ChE', 'CDS', 'CNS', 'CS', 'CE', 'Ec', 'ESL', 'EE', 'E', 'En',
	'ESE', 'EST', 'F', 'FS', 'Ge', 'H', 'HPS', 'Hum', 'L', 'Law', 'Ma', 'MS', 'ME',
	'Mu', 'Pl', 'PE', 'Ph', 'PS', 'PA', 'Psy', 'SS', 'SA', 'Wr', 'CAM',
	'CPH', 'UCL', 'EPT', 'MEL', 'EDN']
	return token[0] in options

def is_units(token, string):
	s = string.split('-')
	is_number = lambda s: is_int(s) or is_float(s)
	return string == '+' or (len(s)==3 and all(map(is_number, s)))

def is_section(token, string):
	return is_int(string)

def is_professor_name(token, string):
	return token[-2][-1] == ',' and token[-1].isupper() and len(token[-1]) == 1

def is_day_time(token, string):

	# first test whether token[0] is a date abbreviation;
	tokenpass = [0, 0, 0, 0]
	tokenpass[0] = is_day_abbreviation(token[0])

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
	"Room POLY",
	"100 - Rock",
	"TR DAB"]

	return token in [initial_parse(s)[0] for s in parts]

def is_annotation(token, string):
	annotations = ["taught",
		"updated",
		"lottery",
		"change in",
		"Permission",
		"graduate students",
		"Maximum",
		"enrollment:",
		"Make-up",
		"cancelled",
		"Most sessions",
		"session",
		"research advisor",
		"Required",
		"Taught",
		"Prerequisite:",
		"lecture time",
		"Lecture Recitation Tutorial",
		"permission",
		"offered",
		"arrangement",
		"Field Trip:",
		"Field Trip",
		"updated",
		"Sec",
		"Formerly",
		"Section",
		"will meet",
		"October.",
		"OM to",
		"Lab tour"
	]
	tokenized_annotations = [initial_parse(ann)[0] for ann in annotations]

	return any([is_sublist_of(tok_ann, token) for tok_ann in tokenized_annotations])



def is_time_start(token, string):
	# first test whether token[0] is a date abbreviation;
	return is_day_abbreviation(token[0])


def is_time_end(token, string):
	is_time = lambda string: all([is_int(part) for part in string.split(':')]) \
		and	len(string.split(':')) == 2
	return is_time(token[0])

def is_course_title(token, string):
	manual_courses = \
	['Introduction to Earth and Planetary Sciences: Earth as a Planet',
	'Freshman Seminar: Albatrosses, Beetles and Cetaceans',
	'Freshman Seminar: Gravitational Waves',
	'Discrete Differential Geometry: Theory and Applications',
	'Intercollegiate Basketball Team (Men)',
	"Undergraduate Research and Bachelor's Thesis",
	"Earth's Atmosphere",
	'18th-Century Philosophy: Locke to Kant',
	"Earth's Oceans",
	'European Civilization: Early Modern Europe',
	'Karate (Shotokan), Beginning and Intermediate/Advanced',
	'Freshman Seminar: Research Tutorial',
	"Men's Glee Club",
	'Freshman Seminar: The Science of Music',
	'Angels and Monsters: Cosmology, Anthropology, and the Ends of the World',
	"Women's Glee Club",
	'The 19th-Century English Novel',
	'Intercollegiate Cross Country Team (Men and Women)',
	'Intercollegiate Water Polo Team (Men & Women)',
	'Intercollegiate Swimming Team (Men and Women)',
	'Freshman Seminar: In Search of Memory',
	'Intercollegiate Volleyball Team (Women)',
	"Master's Thesis Research",
	'Intercollegiate Fencing Team (Men and Women)',
	'Intercollegiate Soccer Team (Men)',
	'European Civilization:  Modern Europe',
	'Freshman Seminar: Earthquakes',
	'Intercollegiate Basketball Team (Women)']


	return all([is_course_word(tok) for tok in token]) or \
		token in [initial_parse(s)[0] for s in manual_courses]

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
	(lambda t, s: [filter(lambda word: len(word) > 0, t), s], 6),
	(lambda t, s: [map(word_number_split, t),s], 7),
	(lambda t, s: [flatten_level_one_list(t), s], 8),
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



def identify_type(line):

	type_list = ["A",
				 "ANNOTATION",
				 "UNITS",
				 "COURSE_NAME",
				 "SECTION",
				 "PROFESSOR_NAME",
				 "GRADE_SCHEME",
				 "DAY_TIME",
				 "LOCATION",
				 "LOCATION_PART",
				 "TIME_START",
				 "TIME_END",
				 "COURSE_TITLE",
				 "UNSURE", # this should always be last
				 "BLANK_LINE"]

	if line == "":
		return "BLANK_LINE"
	[token, string] = initial_parse(line)
	for t in type_list:
		try:
			p = LINE_TYPES[t][0](token, string)
		except IndexError:
			p = False
		if p:
			return t


def parse_course_name(token, string):
	return (token[:-1], token[-1])

def parse_units(token, string):
	if string == "+":
		return (0.0, 0.0, 0.0)
	else:
		# float! not int, to deal with 1.5-0-2.5
		return tuple([float(w) for w in string.split("-")])

def parse_section(token, string):
	return int(string)

def parse_professor(token, string):
	fence_marks = [0] + [a+2 for a in range(len(token)) if ',' in token[a]]

	# remove commas
	token = [tok.rstrip(',') for tok in token]
	return [token[fence_marks[i]: fence_marks[i+1]] for i in range(len(fence_marks) - 1)]

def process_time(t):
	[left, right] = t.split(':')
	if right == '00':
		return int(left)
	elif right == '55':
		return int(left) + 1
	return float(left) + float(right) / 60.0

def process_days(day_string):
	# A 0 will stand for organizational meeting (for now)
    day_to_num = {'M': 1, 'T': 2, 'W': 3, 'R': 4, 'F': 5, 'S': 6}
    return_list = []
    if 'OM' in day_string:
    	s = day_string.replace('OM,', '')
    	return_list = [0]
    for day in s:
    	return_list.append(day_to_num[day])
    # return_list.sort() is this needed?
    return return_list

def parse_day_time(token, string):
    ''' Process the initial tokens with the guess that we are processing
    day/times.

    Sample input: ['MWF', '11:30', '-', '13:55']
    Sample output: [[1, 3, 5], (11.5, 14)]
    '''
    day_list = process_days(token[0])
    start_time, end_time = filter(lambda s: len(s) > 1, token[1:])
    # Gives us filtered = ['11:30', '13:00']
    return [day_list, (process_time(start_time), process_time(end_time))]

def parse_grade_scheme(token, string):
	return string

def parse_location(token, string):
	return string

def parse_annotation(token, string):
	return string

def parse_course_title(token, string):
	return string

def parse_time_start(token, string):
	''' Time start usually has a day_string starting the line.

	Sample input: (['OM,M', '09:00', '-'], 'OM,M 09:00 -')
	Sample output: [[0, 1], 9]
	'''
	day_list = process_days(token[0])
	time = filter(lambda s: re.match('(2[0-3]|0?[0-9]|1[0-9]): ?([0-5][0-9])', s), string.split(' '))
	return [day_list, process_time(time[0])]

def parse_time_end(token, string):
	return process_time(string)

def parse_A(token, string):
	return string

def parse_location_part(token, string):
	return string


def parse_unsure(token, string):
	raise Exception("UNSURE LINE")

# TOOO:
# Write a parser for each of the applicable line types
# below.
#
# for an example of each type, take a look at
# typed_c.txt
#
# add them to the list corresponding to each line type
#
# also take a look at read_caltech_schedule.py
# for a proposed spec.
#
#
# looking forward to your pull requests ...

def action_course_name(data, course):
	# Data is the output of parse_course_name. (['ACM', 'Ma', 'EE'], '095A')
	copy = course.copy()
	copy['option'] = data[0]
	copy['number'] = data[1]
	return copy

def action_course_title(data, course):
	# Data is a course title string.
	copy = course.copy()
	copy['title'] = data
	return copy

def action_section(data, course):
	copy = course.copy()
	if not 'section' in copy.keys():
 		copy['section'] = [data]
 	else:
 		copy['section'] += [data]
	return copy

def action_units(data, course):
	copy = course.copy()
	copy['units'] = data
	return copy

def action_professor_name(data, course):
	copy = course.copy()
	copy['professors'] = data
	return copy

def action_day_time(data, course):
	copy = course.copy()
	if not 'days' in copy.keys():
		copy['days'] = [data[0]]
	else:
		copy['days'] += [data[0]]
	if not 'times' in copy.times():
		copy['times'] = data[1]
	else:
		copy['times'].append(data[1])
	return copy

def action_location(data, course):
	copy = course.copy()
	if not 'locations' in copy.keys():
		copy['locations'] = [data]
	else:
		copy['locations'].append(data)
	return copy

def action_grade_scheme(data, course):
	copy = course.copy()
	copy['grade_scheme'] = data
	return copy

def action_A(data, course):
	''' Ignore A but set default values at beginning? Or set them just before publishing. If the day/time/location keys do not exist before publishing, set them to default values.
	'''
	pass

def action_location_part(data, course):
	copy = course.copy()
	if not 'locations' in copy.keys():
		copy['locations'] = [data]
	else:
		# Append the data we have to the last item in locations
		copy['locations'][-1] += data
	return copy

def action_annotation(data, course):
	copy = course.copy()
	if not 'annotation' in copy.keys():
		copy['annotation'] = [data]
	else:
		copy['annotation'].append(data)
	return copy

def action_unsure(data, course):
	# cry
	pass

def action_time_start(data, course):
	copy = course.copy()
	if not 'days' in copy.keys():
		copy['days'] = [data[0]]
	else:
		course['days'].append(data[0])
	# Initialize the tuple with the start time
	try:
		copy['times'].append((data[1]))
	except(KeyError):
		# Initialize times to a list of one number
		copy['times'] = [data]
	return copy

def action_time_end(data, course):
	# Assumes that the course already has a time start
	copy = course.copy()
	(start, end) = (copy['times'][-1], data)
	copy['times'].pop()
	copy['times'].append((start, end))
	return copy

LINE_TYPES = {"COURSE_NAME" : [is_course_name, parse_course_name, action_course_name],
				  "UNITS" : [is_units, parse_units, action_units],
				  "SECTION" : [is_section, parse_section, action_units],
				  "PROFESSOR_NAME" : [is_professor_name, parse_professor, action_professor_name],
				  "DAY_TIME" : [is_day_time, parse_day_time, action_day_time],
				  "LOCATION" : [is_location, parse_location, action_location],
				  "GRADE_SCHEME" : [is_grade_scheme, parse_grade_scheme, action_grade_scheme],
				  "A" : [is_A, parse_A, action_A],
				  "LOCATION_PART" : [is_location_part, parse_location_part, action_location_part],
				  "ANNOTATION" : [is_annotation, parse_annotation, action_annotation],
				  "TIME_START" : [is_time_start, parse_time_start, action_time_start],
				  "TIME_END" : [is_time_end, parse_time_end, action_time_end],
				  "COURSE_TITLE" : [is_course_title, parse_course_title, action_course_title],
				  "UNSURE": [is_unsure, parse_unsure, parse_unsure]}

def main():
	print initial_parse(argv[1])

if __name__ == '__main__':
	main()