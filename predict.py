'''
This file predicts course enrollments using a linear regression
and writes these predictions to a file
'''

import csv
import cPickle
import numpy as np
from sklearn import linear_model

# the name of the file that contains our pickled dictionary
COURSE_DATA_DICT_FILENAME = "pickled_course_data.txt"

# the name of the file to which we write predictions
COURSE_PREDICTIONS_FILENAME = "course_predictions.csv"

# load our course enrollment data by file
with open(COURSE_DATA_DICT_FILENAME, "r") as f:
		 course_data_dict = cPickle.load(f)

with open(COURSE_PREDICTIONS_FILENAME, "w") as predictions_file:
	
	# prepare CSV file for writing
	writer = csv.DictWriter(predictions_file, 
		fieldnames=["course_id", "year", "fall_prediction", "spring_prediction"])
	writer.writeheader()

	# construct two enrollment lists (one for each term) for each course
	for course_id in course_data_dict:
		enrollment_data_dict = {
			"FALL": [],
			"SPRING": []
		}

		# for each academic year, we will have 2 pieces of data: fall enrollment
		# and spring enrollment
		for academic_year in course_data_dict[course_id]:
			for term in ["FALL", "SPRING"]:
				if term in course_data_dict[course_id][academic_year]:
					enrollment = course_data_dict[course_id][academic_year][term]
					# push in a tuple of academic year and enrollment for that year.
					# ex. (2014, 100)
					enrollment_data_dict[term].append((academic_year, enrollment))

		# now that we have a history enrollments for both FALL and SPRING 
		# semesters, we can begin predicting
		YEAR_TO_PREDICT = 2015

		predicted_enrollments = {
			"FALL": -1,
			"SPRING": -1
		}

		# predict fall enrollments if we have fall data
		for term in ["FALL", "SPRING"]:
			if len(enrollment_data_dict[term]) > 0:
				regr = linear_model.LinearRegression()
				
				x_train = np.array([int(pairing[0]) for pairing in enrollment_data_dict[term]]).reshape(-1, 1)
				y_train = np.array([int(pairing[1]) for pairing in enrollment_data_dict[term]]).reshape(-1, 1)
				regr.fit(x_train, y_train)

				predictions = regr.predict(np.array([YEAR_TO_PREDICT]).reshape(1, -1))
				predicted_enrollments[term] = round(predictions[0][0], 3)

		# write predictions to a file
		prediction_csv_row = {
			"course_id": course_id,
			"year": YEAR_TO_PREDICT,
			"fall_prediction": predicted_enrollments["FALL"],
			"spring_prediction": predicted_enrollments["SPRING"]
		}

		writer.writerow(prediction_csv_row)
		print prediction_csv_row
