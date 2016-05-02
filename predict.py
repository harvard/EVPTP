'''
This file predicts course enrollments using a linear regression
and writes these predictions to a file.

To predict course enrollments for 2015, simply run `python predict.py`
'''

import csv
import cPickle
import numpy as np
from sklearn import linear_model

# the name of the file that contains our pickled dictionary
COURSE_DATA_DICT_FILENAME = "pickled_course_data.txt"

# the name of the file to which we write predictions
COURSE_PREDICTIONS_FILENAME = "course_predictions.csv"

# our pickled dictionary has data up until 2014, so we want to predict
# enrollments for 2015
YEAR_TO_PREDICT = 2015

# load our course enrollment data by file
with open(COURSE_DATA_DICT_FILENAME, "r") as f:
		 course_data_dict = cPickle.load(f)

with open(COURSE_PREDICTIONS_FILENAME, "w") as predictions_file:
	
	# prepare CSV file for writing
	writer = csv.DictWriter(predictions_file, 
		fieldnames=["course_id", "year", "fall_prediction", "spring_prediction"])
	# write the fieldnames to the header of the CSV
	writer.writeheader()

	for course_id in course_data_dict:
		# construct two enrollment lists (one for each term) for each course
		enrollment_data_dict = {
			"FALL": [],
			"SPRING": []
		}

		# for each academic year, we will have 2 pieces of data: fall enrollment
		# and spring enrollment
		for academic_year in course_data_dict[course_id]:
			for term in ["FALL", "SPRING"]:
				if term in course_data_dict[course_id][academic_year]:
					# grab the enrollment from the unpickled dictionary
					enrollment = course_data_dict[course_id][academic_year][term]
					# push in a tuple of academic year and enrollment for that year.
					# ex. (2014, 100)
					enrollment_data_dict[term].append((academic_year, enrollment))

		# a dictionary to hold our predictions for the given course
		predicted_enrollments = {
			"FALL": -1,
			"SPRING": -1
		}

		# predict fall enrollments if we have fall data
		for term in ["FALL", "SPRING"]:
			# if we actually have data to predict on...
			if len(enrollment_data_dict[term]) > 0:
				regr = linear_model.LinearRegression()
				
				# grab all the years
				x_train = np.array([int(pairing[0]) for pairing in enrollment_data_dict[term]]).reshape(-1, 1)
				# grab all the enrollments
				y_train = np.array([int(pairing[1]) for pairing in enrollment_data_dict[term]]).reshape(-1, 1)

				# fit the data
				regr.fit(x_train, y_train)

				# now predict the YEAR_TO_PREDICT
				predictions = regr.predict(np.array([YEAR_TO_PREDICT]).reshape(1, -1))

				# add the predictions to the predicted_enrollments dictionary
				predicted_enrollments[term] = round(predictions[0][0], 3) # round to 3 decimal places

		# to be written to a file
		prediction_csv_row = {
			"course_id": course_id,
			"year": YEAR_TO_PREDICT,
			"fall_prediction": predicted_enrollments["FALL"],
			"spring_prediction": predicted_enrollments["SPRING"]
		}

		writer.writerow(prediction_csv_row)
		print prediction_csv_row
