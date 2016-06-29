'''
Compares predictions for 2015 against actual enrollments and reports statistics. 
'''

import csv
import numpy as np

# dictionaries to hold the two sets of values we want to compare
predictions = {}
real_enrollments = {}

# read the predictions into a dictionary
with open("course_predictions.csv", "r") as predictions_csv:
	csv_r = csv.DictReader(predictions_csv)
	for row in csv_r:
		course_id = row["course_id"]
		predictions[course_id] = {}
		predictions[course_id]["FALL_PREDICTION"] = row["fall_prediction"]
		predictions[course_id]["SPRING_PREDICTION"] = row["spring_prediction"]

# read the enrollments into a dictionary
with open("NewData/FAS2015-16CourseEnrollments.csv", "r") as real_enrollments_csv:
	csv_r = csv.DictReader(real_enrollments_csv)
	for row in csv_r:
		course_id = row["CRSE_ID"]
		enrollment = row["ENROLLMENT"]
		semester = "FALL"
		real_enrollments[course_id] = {}
		real_enrollments[course_id][semester] = enrollment

# holds differences between predicted and actual enrollments
diffs = np.array([])

# calculate differences
for course_id_pred, enroll_pred in predictions.iteritems():
	if course_id_pred in real_enrollments:
		real_enrollment = real_enrollments[course_id_pred]["FALL"]
		diffs = np.append(diffs, abs(enroll_pred - real_enrollment))

# print "Avg diff: ", diffs.mean()