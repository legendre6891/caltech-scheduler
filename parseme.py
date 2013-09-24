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
	initial_parse_functions = [
	[lambda s: s.split(' '), 1],
	[lambda t, s: [map(word_number_split, t),s], 2],
	[lambda t, s: [flatten_level_one_list(t), s], 3]
	]


	token = initial_parse_functions[0][0](current_line)
	[token, current_line] = initial_parse_functions[1][0](token, current_line)
	[token, current_line] = initial_parse_functions[2][0](token, current_line)

	return [token, current_line]



def main():
	print initial_parse(argv[1])



if __name__ == '__main__':
	main()