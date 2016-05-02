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
import csv

# the name of the file that contains our pickled dictionary
COURSE_DATA_DICT_FILENAME = "pickled_course_data.txt"

# the name of the file from which to create the dictionary
IN_FILENAME = \
	"../data/2014-10-09 Course Enrollment Data for PTP Project_Jim Waldo.csv"

# our master dictionary, to be pickled
course_data_dict = {}

def parse_date(dateToParse):
	'''
	Year and term data is concatenated in IN_FILENAME. For example, a course
	that takes place during term 0 of year 2004 has "20040" in CSV pointed to 
	by IN_FILENAME. 
	
	This function parses these concatenated dates into two pieces 
	(e.g., "20040" into 2004 and 0) and returns both pieces of data.

	dataToParse: a string concatenation of a year (e.g., 2004) and a term (1, 2) 
	returns: a separated year and term (e.g., 2004 and FALL) as strings
	'''
	year = dateToParse[:-1]
	
	# use human-readable strings instead of "1" and "2" for term
	if dateToParse[-1:] is "1":
		term = "FALL"
	else:
		term = "SPRING"

	return year, term

def pickle_and_save():
	'''
	Pickles our master course dictionary and saves it to 
	COURSE_DATA_DICT_FILENAME
	'''
	with open(COURSE_DATA_DICT_FILENAME, "w") as f:
		cPickle.dump(course_data_dict, f)

def unpickle_and_print():
	'''
	Deserializes our pickled course dictionary and prints it to the console
	'''
	with open(COURSE_DATA_DICT_FILENAME, "r") as f:
		print cPickle.load(f)

# construct the dictionary
with open(IN_FILENAME) as f:
	# create a CSV reader object
	reader = csv.reader(f, delimiter='\t')
	
	# skip the first line so we don't read in the CSV header
	reader.next()
	
	for row in reader:	
		# row[1] represents the concatanted date that needs parsing (e.g. "20041")
		year, term = parse_date(row[1])
		course_id = row[2]

		# construct the dictionary by checking for keys and incrementing
		# when necessary. We only need to increment when the full dictionary
		# path to a course already exists (e.g., when the data structure already
		# has keys for the course_id, the year, and the term)
		
		# check if course_id already exists in the dictionary
		if course_id in course_data_dict:
			# check if the year for a given course_id exists
			if year in course_data_dict[course_id]:
				# check if a term for a given year for a given course exits
				if term in course_data_dict[course_id][year]:
					# if so, increment the enrollment by 1
					course_data_dict[course_id][year][term] += 1 
				else:
					course_data_dict[course_id][year][term] = 1
			else:
				course_data_dict[course_id][year] = {}
				course_data_dict[course_id][year][term] = 1
		else:
			course_data_dict[course_id] = {}
			course_data_dict[course_id][year] = {}
			course_data_dict[course_id][year][term] = 1

pickle_and_save()
unpickle_and_print()
