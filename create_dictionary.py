'''
This program consumes the data files used in PTP prediction
attempts to build a multi-level dictionary that has the following form:

{
	course_id: {
		academic_year: {
			term: `enrollment for course_id during term of academic_year`
		}
	}
}

The program can also be used to add new information to the dictionary; if an existing file with a dictionary
is given as the output file, the dictionary is first read, and a set of the courseId+Year+Term is created and
records for those existing entries will not be calculated

Imports cPickle, a serialization library for Python objects. This package is
used to pickle our master course dictionary into a byte_stream saved as a 
txt file. Imports csv to read the input file, sys to get the command-line arguments, and
os.path to determine if the pickle file already exists.

'''
import cPickle
import csv, sys, os.path

def get_csv(infile_name):
    '''
    Take an input string naming an existing file and create a csv reader for the file. Part of
    this routine will determine the delimiter used in the file, as we have been getting both
    comma- and tab-separated files for our data.
    :param infile_name: Name of an existing file containing a csv-formatted course enrollment data
    :return: A csv-reader that is set to the appropriate delimiter.
    '''
    inf = open(infile_name, 'r')
    dialect = csv.Sniffer().sniff(inf.read(1024))
    inf.seek(0)
    csv_r = csv.reader(inf, delimiter=dialect.delimiter)
    return csv_r

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


def pickle_and_save(course_data_dict, outf):
    '''
    Pickles our master course dictionary and saves it to the file named by outf. If this file
    already exists, it will be over-written by the newly constructed dictionary.
    '''
    wfile = open(outf, 'w')
    cPickle.dump(course_data_dict, wfile)
    wfile.close()


def unpickle_and_print(from_file):
    '''
    Deserializes our pickled course dictionary and prints it to the console
    '''
    with open(from_file, "r") as f:
        print cPickle.load(f)

def unpickle_and_build_set(pickle_file):
    '''
    Opens the file named by the parameter and reconstructs the dictionary that was pickled in that file. Using that
    dictionary, builds a set of concatenated courseId/Year/term that are in a dictionary, so that those courses will not
    have thier enrollment counted (actually, added to) by the main() function.
    :param pickle_file: name of the file containing the pickle of the dictionary that already exists and is being
    added to
    :return: A pair of a dictionary as specified at the beginning of the file, and a set whose entries are the
    concatenation of courseId/Year/Term that already appear in the dictionary
    '''
    r = open(pickle_file, 'r')
    course_data_dict = cPickle.load(r)
    course_set = set()
    r.close()
    for k, v in course_data_dict.iteritems():
        for y, v1 in v.iteritems():
            for t, v2 in v1.iteritems():
                course_set.add(''.join((k, y, t)))

    return course_data_dict, course_set


def main(reader, course_data_dict, course_set, out_file):
    '''
    Takes an open csv.reader, a dictionary, a set containing course/year/term already in the dictionary,
    and the name of a file to write the pickle of the full
    dictionary, and extracts the dictionary of course information needed from the csv file, writing
    it to the dictionary. The dictionary may be empty or may have previous entries in it; if there are
    previous entries this is assumed to be an addition to the dictionary
    :param reader: an open csv reader containing the class enrollment information
    :param course_data_dict: a dictionary, as specified in the header of this program. If empty, we are
    creating a whole new dictionary; if it is not empty we are appending the an existing data set
    :param course_set: a set containing the concatenated course/year/term groupings that are already in the dictionary
    :param out_file: The name of the output file; this is where the pickle of the final dictionary will
    be placed
    :return: None
    '''
    # construct the dictionary
    # skip the first line so we don't read in the CSV header
    reader.next()
    for row in reader:
        # row[1] represents the concatanted date that needs parsing (e.g. "20041")
        year, term = parse_date(row[1])
        course_id = row[2]
        #first, check to see if this is in the dictionary already; if not add it
        if ''.join((course_id, year, term)) not in course_set:
            # construct the dictionary by checking for keys and incrementing
            # when necessary. We only need to increment when the full dictionary
            # path to a course already exists (e.g., when the data structure already
            # has keys for the course_id, the year, and the term)

            # check if course_id does not exists in the dictionary, if so create an entry and a dictionary
            # as its value
            if course_id not in course_data_dict:
                course_data_dict[course_id] = {}
            # check if the year is in the dictionary for the course id; if not create an entry with a
            # dictionary as its value.
            if year not in course_data_dict[course_id]:
                course_data_dict[course_id][year] = {}
            # check if the term is in the dictionary for the course and year; if not create an entry and
            # initialize the count to one
            if term not in course_data_dict[course_id][year]:
                course_data_dict[course_id][year][term] = 1
            else:
                # if the course/year/term is in the dictionary, increment the count for that entry
                course_data_dict[course_id][year][term] += 1

    pickle_and_save(course_data_dict, out_file)
    #unpickle_and_print(out_file)


if __name__ == '__main__':
    in_data = sys.argv[1]
    if not os.path.exists(in_data):
        print 'Specified input file does not exist'
        print 'Usage: python create_dictionary.py class_file.csv output_dictionary'
        exit(1)

    csv_in = get_csv(in_data)

    out_file = sys.argv[2]
    if os.path.exists(out_file):
        course_data_dict, course_set =unpickle_and_build_set(out_file)
    else:
        course_data_dict = {}
        course_set = set()

    main(csv_in, course_data_dict, course_set, out_file)
