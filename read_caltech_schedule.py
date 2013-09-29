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
	def __init__(self, bchunk):
		super(CourseChunk, self).__init__()
		self.sections = split_list(bchunk, lambda c: identify_type(c) == 'SECTION')[1:]
		self.chunks = bchunk

	def singleton(self, xs, line_type):
		try:
			return [line for line in xs if identify_type(line) == line_type][0]
		except:
			raise IndexError("Singleton not found")
			

	def multiton(self, xs, line_types):
		return [line for line in xs if identify_type(line) in line_types]


	@property
	def section_count(self):
		s = 'SECTION'
		return max([LINE_TYPES[s][1](*initial_parse(line)) for line in self.chunks if identify_type(line) == s])

	@property
	def options(self):
		s = 'COURSE_NAME'
		return LINE_TYPES[s][1](*initial_parse(self.singleton(self.chunks, s)))[0]

	@property
	def number(self):
		s = 'COURSE_NAME'
		return LINE_TYPES[s][1](*initial_parse(self.singleton(self.chunks, s)))[1]

	@property
	def title(self):
		s = 'COURSE_TITLE'
		return LINE_TYPES[s][1](*initial_parse(self.singleton(self.chunks, s)))

	@property
	def units(self):
		s = 'UNITS'
		return LINE_TYPES[s][1](*initial_parse(self.singleton(self.chunks, s)))

	@property
	def annotations(self):
		s = ['ANNOTATION']
		lines = self.multiton(self.chunks, s)
		return ' '.join([LINE_TYPES['ANNOTATION'][1](*initial_parse(line)) for line in lines])

	def get_locations(self, section):
		s = 'LOCATION'
		t = 'LOCATION_PART'

		locations = self.multiton(self.sections[section], [s])
		parts = self.multiton(self.sections[section], [t])


		# LOCATION_PART should come first to match sections correctly!!
		merged = [' '.join(parts)] + locations

		if merged == ['']:
			return ['A']
		return merged

	def get_grade_scheme(self, section):
		s = 'GRADE_SCHEME'
		try:
			line = self.singleton(self.sections[section], s)
			return line
		except:
			return "EITHER"

	def get_professors(self, section):
		s = 'PROFESSOR_NAME'
		line = self.singleton(self.sections[section], s)
		return LINE_TYPES[s][1](*initial_parse(line))

	def get_day_time(self, section):
		s = 'DAY_TIME'
		t = 'TIME_START'
		u = 'TIME_END'

		normal_lines = self.multiton(self.sections[section], [s])
		start_lines = self.multiton(self.sections[section], [t])
		end_lines = self.multiton(self.sections[section], [u])

		merge = [' '.join(a) for a in zip(start_lines, end_lines)] + normal_lines

		if merge == []:
			return ['A']
		return [LINE_TYPES['DAY_TIME'][1](*initial_parse(a)) for a in merge]


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
			if chunk[0] == "Ma 290":
				tt = CourseChunk(chunk)
		except:
			raise ValueError("Class not found")

	print 'sec len:', tt.section_count
	print 'options:', tt.options
	print 'units:', tt.units
	print 'title:', tt.title
	print 'number', tt.number
	print 'annotations:', tt.annotations
	print 'location of section 1:', tt.get_locations(0)
	print 'grade of section 1:', tt.get_grade_scheme(0)
	print 'professor of section 1:', tt.get_professors(0)
	print 'times of section 1:', tt.get_day_time(0)
	# totality_courses = flatten_level_one_list([process_chunk(chunk) for chunk in chunks])
	return

if __name__ == '__main__':
	main()