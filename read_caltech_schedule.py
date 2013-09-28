#!/usr/bin/env python
from sys import argv
from parseme import *
from pprint import pprint


class CaltechCourse(object):
	"""docstring for CaltechCourse"""
	def __init__(self):
		super(CaltechCourse, self).__init__()
		self.id = -1
		self.year = 2014
		self.season = "FALL"
		self.options = []
		self.number = "999A"
		self.title = "Booty Hovse is the best"
		self.sections = []
		self.units = (0, 0, 0)
		self.professors = []
		self.days = []
		self.organizational_meeting = False
		self.times = []
		self.locations = []
		self.grade_scheme = "EITHER"
		self.annotations = []
		self.notes = []

	def to_JSON(self):
		raise NotImplementedError

class CourseChunk(object):
	"""docstring for CourseChunk"""
	def __init__(self, chunk):
		super(CourseChunk, self).__init__()
		self.chunk = chunk

	def singleton(self, line_type):
		return [line for line in self.chunk if identify_type(line) == line_type][0]


	def multiton(self, line_types):
		return [line for line in self.chunk if identify_type(line) in line_types]


	@property
	def section_count(self):
		s = 'SECTION'
		return max([LINE_TYPES[s][1](*initial_parse(line)) for line in self.chunk if identify_type(line) == s])

	@property
	def options(self):
		s = 'COURSE_NAME'
		return LINE_TYPES[s][1](*initial_parse(self.singleton(s)))[0]

	@property
	def number(self):
		s = 'COURSE_NAME'
		return LINE_TYPES[s][1](*initial_parse(self.singleton(s)))[1]

	@property
	def title(self):
		s = 'COURSE_TITLE'
		return LINE_TYPES[s][1](*initial_parse(self.singleton(s)))

	@property
	def units(self):
		s = 'UNITS'
		return LINE_TYPES[s][1](*initial_parse(self.singleton(s)))

	@property
	def annotations(self):
		s = ['ANNOTATION']
		lines = self.multiton(s)
		return ' '.join([LINE_TYPES['ANNOTATION'][1](*initial_parse(line)) for line in lines])

def split_list(xs, criterion):
	"""
	Chop up the list `xs' based on `criterion'

	For example:
	xs = [A, A, A, X, A, X, A, X, X, A]
	  where criterion(X) is true, criterion(A) is false.

	the output is:
	[[A, A, A], [X, A], [X, A], [X], [X, A]]
	"""

	fence_posts = [a for a in range(len(xs)) if criterion(xs[a])] + [len(xs)]
	if 0 not in fence_posts:
		fence_posts = [0] + fence_posts
	return [xs[fence_posts[i]:fence_posts[i+1]] for i in range(len(fence_posts)-1)]


def main():

	with open(argv[1], "r") as f:
		lines = [line.rstrip() for line in f if line.strip() != '']


	print "Chunking the file ... this may take some time"
	chunks = split_list(lines, lambda l: identify_type(l) == 'COURSE_NAME')
	print "DONE"

	for index, chunk in enumerate(chunks):
		try:
			if chunk[0] == "BMB/Ch 202A":
				tt = CourseChunk(chunk)
		except:
			print index
			print chunk[index-1]

	print 'sec len:', tt.section_count
	print 'options:', tt.options
	print 'units:', tt.units
	print 'title:', tt.title
	print 'number', tt.number
	print 'annotations:', tt.annotations
	# totality_courses = flatten_level_one_list([process_chunk(chunk) for chunk in chunks])
	return

def process_lines(lines):
	''' Process the lines from a single course, creating the dictionary for this course.
	Note: each entry in lines is a tuple of the form (line, line_type)
	'''
	course = {'id': current_id}
	for (line, line_type) in lines:
		token, string = initial_parse(line)
		parse_result = LINE_TYPES[line_type][1](token, string)
		# action
		LINE_TYPES[line_type][2](parse_result, course)
	caltech_courses.append(course)

if __name__ == '__main__':
	main()