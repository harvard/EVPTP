'''
This program consumes some of the data files used in past PTP prediction
attempts to build a multi-level dictionary that has the following form:

{
	course_id: {
		academic_year: {
			term: `enrollment for course_id during term of academic_year`
		}
	}
}

Imports cPickle, a serialization library for Python objects. This package is
used to pickle our master course dictionary into a byte_stream saved as a 
txt file.

'''
import cPickle

DATA_FILE = "course_data.txt"

data = {}
data[1] = 2
data[4] = 5

with open(DATA_FILE, "w") as f:
	cPickle.dump(data, f)

with open(DATA_FILE, "r") as f:
	lol = cPickle.load(f)
	print lol