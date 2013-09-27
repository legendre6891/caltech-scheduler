#!/usr/bin/env python


from sys import argv
from parseme import *
from pprint import pprint


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


course_options = \
['Ae', 'An', 'ACM', 'AM', 'APh', 'Art', 'Ay', 'BMB', 'BE', 'Bi',
 'BEM', 'Ch', 'ChE', 'CDS', 'CNS', 'CS', 'CE', 'Ec', 'ESL', 'EE', 'E', 'En',
 'ESE', 'EST', 'F', 'FS', 'Ge', 'H', 'HPS', 'Hum', 'L', 'Law', 'Ma', 'MS', 'ME',
 'Mu', 'Pl', 'PE', 'Ph', 'PS', 'PA', 'Psy', 'SS', 'SA', 'Wr', 'CAM',
 'CPH', 'UCL', 'EPT', 'MEL', 'EDN']

# A caltech_course is a *dictionary* with the following fields:
# -------------------------------------------------------------
# id;
#   a string, unique to each course
#
# year;
#   an integer, denoting the year the class was held in
#
# season;
#   one of the strings "FALL", "WINTER", "SPRING"
#
# option;
#   a list of strings e.g. ["ACM", "Ma"];
#   it shall follow option naming given above
#
# number;
#   a *string* such as "108A", optionally ending in a number
#
# title;
#   a title, e.g. "Electricity and Magnetism"
#
# section;
#   an integer
#
# units;
#   a *tuple* of three numbers, e.g. (3,0,6); + is coerced to (0,0,0)
#
# professors;
#   a list whose numbers of pairs of strings, e.g. [("Vanier", "M")]
#
# days;
#   a list of lists of 1-7, e.g. [[1,3,5], [2]];
#   an empty list denotes 'Arranged'
#
# organizational_meeting:
#   one of the values {true, false}
#
# times;
#   a list of pairs, e.g. [(10.5, 12), (13, 14)]; empty denotes 'Arranged'
#
# locations;
#   a list of strings, e.g. ["BAX Auditorium", "SLN 51"];
#   empty denotes 'Arranged'
#
# grade_scheme;
#   one of the strings "LETTER", "PASS-FAIL", "EITHER"
#
# annotation;
#   a list of strings, e.g. ["Maximum Enrollment: 14 students"]
#
# notes;
#   a list of strings, e.g. ["I hate this course"]
#



caltech_courses = []
current_id = 0

def main():

	with open(argv[1], "r") as f:
	    lines = f.readlines()

	course_exceptions = []
	writeout = []
	for line in lines:
		line = line.rstrip()
		t = identify_type(line)
		if t == 'COURSE_NAME':
			process_lines(writeout)
			current_id += 1
			writeout = [(line, t)]
		writeout.append((line, t))
		''' TODO:
		Append lines to writeout until we reach a course title.

		Then send writeout to process_lines, and reset writeout, appending the new course title to it.

		Rinse and repeat until EOF?
		'''
		# print identify_type(line) + "|-->>  " + line
		# if identify_type(line) == "UNSURE":
		# 	course_exceptions.append(line)

	# pprint(list(set(course_exceptions)))

def process_lines(lines):
	''' Process the lines from a single course, creating the dictionary for this course.
	Note: each entry in lines is a tuple of the form (line, line_type)
	'''
	course = {'id': current_id}
	state = 'course'
	for (line, line_type) in lines:
		token, string = initial_parse(line)
		if state == 'course':
			parse_result = LINE_TYPES[line_type][1](token, string)
			# action
			LINE_TYPES[line_type][2](parse_result, course)

if __name__ == '__main__':
	main()