import re
from sys import argv


def word_number_split(word):
	match = re.match(r"([a-z]+)([0-9]+)", word, re.I)
	if match:
		items = match.groups()
	else:
		items = [word]

	return list(items)

def flatten_level_one_list(xs):
	return [a for b in xs for a in b]


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


	return [token, current_line]



def main():
	print initial_parse(argv[1])



if __name__ == '__main__':
	main()