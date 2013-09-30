from read_caltech_schedule import CaltechCourse
import cPickle as pickle
import json

def main():
	totality_courses = pickle.load( open( "c.p", "rb" ) )

	for i in range(len(totality_courses)):
		totality_courses[i].id = "FA2013-" + str(i)

		print json.dumps(totality_courses[i].to_JSON(), sort_keys=True,
	                  indent=4, separators=(',', ': ')) + ','



if __name__ == '__main__':
	main()