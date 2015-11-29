__author__ = "Janet Ye, Shantanu Joshi"

import os
import xlrd
import csv
import pandas as pd
import numpy as np
import warnings


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
# '/Users/janetye/Desktop/Attendance'
ABACUS = ROOT_DIR + '/abacus.xlsx'
class Abacus(object):
	def __init__(self, club_dir, filename_list):
		self.club = club_dir
		self.events = filename_list
		self.total_event = 0
		self.total_attendance = 0
		if '.DS_Store' in self.events:
			self.events = self.events[1:]


	def clean_xlsx(self):
		# pass in a club dir
		for filename in self.events:
			if filename[-5:] == ".xlsx":
				self.total_event += 1
				wb = xlrd.open_workbook(self.club+'/'+filename)
				sh = wb.sheet_by_name('Participation')
				output_csv = open(self.club + '/' + filename[:-5] + '.csv', 'wb')
				wr = csv.writer(output_csv, quoting = csv.QUOTE_ALL)

				for rownum in xrange(sh.nrows):
					wr.writerow(sh.row_values(rownum))
				output_csv.close()

	def csv_to_master_df(self, filename_name):
		master_df = pd.DataFrame()
		self.unique_attendee = {}
		for filename in filename_name:
			if filename[-4:] == '.csv':
				email_list = []
				with open(self.club+'/'+filename) as f:
					reader = csv.reader(f)
					body = list(reader)

				event_date = body[1][0][:10]
				event_date = event_date[5:10] + '-' + event_date[:4]
				for row in body:
					if row <> body[0]:
						temp_email = row[4][:row[4].find('@')]
						email_list.append(temp_email)
						if temp_email not in self.unique_attendee.keys():
							self.unique_attendee[temp_email] = 1
						else:
							self.unique_attendee[temp_email] += 1
				self.total_attendance += len(email_list)
				email_list.insert(0, len(email_list))
				email_list.insert(0, event_date)
				email_list.insert(0, len(self.unique_attendee))
				#temp_df = pd.DataFrame(pd.Series(email_list))
				#master_df[event_date] = pd.Series(email_list)
				master_df= pd.concat([master_df, pd.DataFrame(pd.Series(email_list))], ignore_index = True, axis = 1)
		unique_for_output = ['Total Unique Attendee', len(self.unique_attendee), 'Unique Attendee'] + self.unique_attendee.keys()
		master_df = pd.concat([master_df, pd.DataFrame(pd.Series(unique_for_output))], ignore_index = True, axis = 1)
		return master_df

	def summary_sheet(self, club_name):
		try:
			average_attendance = self.total_attendance / self.total_event
		except ZeroDivisionError:
			average_attendance = "Club has no events..."
		average_unique_attendee = np.mean(self.unique_attendee.values())
		row = [club_name, self.total_event, len(self.unique_attendee), average_attendance, average_unique_attendee, average_unique_attendee / self.total_event]
		return row

def main():
	# temp just gets what os outputs..ready to manipulate
	temp = [item for item in os.walk(ROOT_DIR)]
	# default set to individual club
	
	# get a list of club names
	club_names = temp[0][1]

	# manipulate temp, to get club directories
	club_dir = [item[0] for item in temp]
	club_dir = club_dir[1:]

	i=0
	writer = pd.ExcelWriter(ABACUS)

	summary_df = pd.DataFrame(columns = ['Club_Name', 'Total_Event', 'Unique_Attendee', 'Average_Attendance', 'Average_Attendance_Per_Member', 'Retention'], index = np.array(xrange(len(club_dir))))
	for club in club_dir:	
		print '====== PROCESSING', club_names[i], '======'
		filename_list = os.listdir(club)
		club_abacus = Abacus(club, filename_list)

		club_abacus.clean_xlsx()

		filename_list = os.listdir(club)
		club_abacus.csv_to_master_df(filename_list).to_excel(writer, club_names[i])

		summary_df.loc[i] = club_abacus.summary_sheet(club_names[i])
		i += 1
		#warnings.filterwarnings('ignore', 'Mean of empty slice')
	summary_df.to_excel(writer,'Summary')
	writer.save()
	print '====== COMPLETE ======'
if __name__ == '__main__':
	main()

