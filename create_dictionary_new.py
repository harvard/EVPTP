'''
This program consumes the data files used in PTP prediction attempts to build a multi-level dictionary that has the following form:

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

Much of this program is taken from create_dictionary.py; the difference is that this program works with the
data format generated by the new SIS, which is somewhat different from that generated by the old SIS and used
in the other program.
'''

import cPickle, create_dictionary
import csv, sys, os.path

def parse_new_date(dateToParse):
    '''
    Takes the four character string where the first three characters represent the year (with the second digit
    implicit, so 215 = 2015) and the last digit represents the month the course term starts (so 8 = Fall term and
    2 = Spring term) and returns the full year and the term
    :param dateToParse: A four-character string, where the first 3 characters are the year and the last represents the term
    :return: A four-character year, and the term as either 'FALL' or 'SPRING'

    '''
    if dateToParse[0] == '2':
        ins_char = '0'
    else:
        ins_char = '9'
    year = ''.join((dateToParse[0], ins_char, dateToParse[1:3]))
    if dateToParse[:1] == '2':
        term = "SPRING"
    else:
        term = "FALL"

    return year, term


def main(reader, course_data_dict, course_set, out_file):
    '''

    :param reader:
    :param course_data_dict:
    :param course_set:
    :param out_file:
    :return:
    '''

    reader.next()
    for row in reader:
        if row[9] == '0':
            continue

        year, term = parse_new_date(row[2])
        course_id = row[0]
        if ''.join((course_id, year, term)) not in course_set:
            if course_id not in course_data_dict:
                course_data_dict[course_id] = {}
            if year not in course_data_dict[course_id]:
                course_data_dict[course_id][year] = {}
            if term not in course_data_dict[course_id][year]:
                course_data_dict[course_id][year][term] = row[9]
            else:
                course_data_dict[course_id][year][term] += row[9]

    create_dictionary.pickle_and_save(course_data_dict, out_file)

if __name__ == '__main__':
    in_data = sys.argv[1]
    out_file = sys.argv[2]

    if not os.path.exists(in_data):
        print 'Specified input file does not exist'
        print 'Usage: python create_dictionary.py class_file.csv output_dictionary'
        exit(1)

    csv_in = create_dictionary.get_csv(in_data)

    if os.path.exists(out_file):
        course_data_dict, course_set = create_dictionary.unpickle_and_build_set(out_file)
    else:
        course_data_dict = {}
        course_set = set()

    main(csv_in, course_data_dict, course_set, out_file)
