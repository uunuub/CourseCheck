#!/Users/unumunkhb/miniconda3/envs/py27/bin/python

import re, urllib2, smtplib, time, optparse
import urllib3.contrib.pyopenssl

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from subprocess import Popen, PIPE

urllib3.contrib.pyopenssl.inject_into_urllib3()
urllib3.disable_warnings()

# Semester number and search interval
interval = 60
term = 201920

# Course IDs, emails to send and receive
crns = [22505]#, 11717]
receivers = []

# Get sendmail path
sendmailPath = Popen(["which", "sendmail"], stdout=PIPE).communicate()[0][:-1]

def getCourseNames():
	return dict()

def getCRN(courseName):
	return ""

def sendEmail(receivers, subject, message):
	#Form the email message without receiver
	msg = MIMEMultipart()
	msg["Subject"] = subject
	msg.attach(MIMEText(message))
	
	# Send to all receivers 
	for email in receivers:
		# Change receivers	
		msg["To"] = email
		# Send mail
		p = Popen([sendmailPath, "-t", "oi"], stdin=PIPE)
		p.communicate(msg.as_string())	
		

def getAvailable(crn):
	# Form url of course web page
	http = urllib3.PoolManager()
	url = 'https://selfservice.mypurdue.purdue.edu/prod/bwckschd.p_disp_detail_sched?term_in={}&crn_in={}'.format(term, crn)
	r = http.request('GET', url)
	data = r.data   

	# Print out url for course web page
	print(url)

	# Find table entry of "Seats"
	pattern = "<td class=\"dddefault\">([0-9]*)</td>.*?<td class=\"dddefault\">([0-9]*)</td>.*?<td class=\"dddefault\">([0-9]*)</td>"
	# Matches will be 3 rows: Seats, Waitlist Seats, Cross List Seats
	# 1st row has 3 columns: Capacity, Actual, Remaining	
	matches = re.findall(pattern, data, re.MULTILINE + re.DOTALL + re.I)	
	# Return Remaining Seats	
	return matches[0][2]
	
def loop(nameToCrn):
	# Reverse dictionary
	crnToName = {v: k for k, v in nameToCrn.iteritems()}
	crnFound = {v: 0 for k, v in nameToCrn.iteritems()}
	
	# Number of courses
	cycled = 0

	# FOREVERRRRR
	while True:
		# Go through crn list
		for crnList in crnToName:
			print("course name: {}".format(crnToName[crnList]))
			print("crn: {}".format(crnList[crnFound[crnList]]))

			# Get open seats of current course id
			openSeats = getAvailable(crnList[crnFound[crnList]])	
			if openSeats > 0: #When it is open
				subject = "{courseName}: {seats} available seats".format(courseName=crnToName[crnList], seats=openSeats)	
				message = "{courseName}: {seats} available seats".format(courseName=crnToName[crnList], seats=openSeats)
				sendEmail(receivers, subject, message)
	
			# Increment iteartor
			crnFound[crnList] += 1
			cycled += 1

			# Reset iterator through a course
			if crnFound[crnList] >= len(crnList):
				crnFound[crnList] = 0
					
			# Sleep after one check through has been went through
			if cycled >= len(crnToName):
				time.sleep(interval * 60)
			# Else just sleep to not get blacklisted
			else:
				time.sleep(60)
					


if __name__ == "__main__":
	# Stop if email script wasn't found
	if sendmailPath == "":
		print("sendmail not found. exiting.")
		exit(0)
	
	# Settings to parse command line args
	parser = optparse.OptionParser()
	# Add receivers list flag
	parser.add_option("--receivers", action="store", 
                  default="receivers.txt", 
                  dest="recs",
                  help="file containing newline separated recipient emails",
                  )
	# Add course list flag
	parser.add_option("--courses", action="store", 
                  default="courses.txt", 
                  dest="courses",
                  help="file containing newline separated course names",
                  )
	# Parse command line arguments 
	options, args = parser.parse_args()

	# Add recipeints to list
	with open(options.recs) as f:
		content = f.readlines()
	receivers = [x.strip() for x in content] 

	nameID = {"cs381": (36593, ), 
			  "cs348": (13073, ),
			  "cs354": (13032, ), 
			  "stat416": (10702, 11324, 16388)}
	loop(nameID)

