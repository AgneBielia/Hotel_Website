from flask import Flask, render_template
from flask import request
import csv
from time import gmtime, strftime

app = Flask(__name__)
# ************** HOMEPAGE, Reviews***********************************#


@app.route('/', methods=['GET'])
def home():
    # read the reviewList from file
    reviewFile = 'static/reviewList.csv'
    reviewList = readFile(reviewFile)
    return render_template('index1.html',  reviewList=reviewList)


@app.route('/addEntry', methods=['POST'])
def addEntry():

    # read the reviewList from file
    reviewFile = 'static/reviewList.csv'
    reviewList = readFile(reviewFile)

    # add the new entry
    userName = request.form[('name')]
    review = request.form[('review')]
    rating = request.form[('star')]
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    newEntry = [time, userName, review, rating]
    reviewList.append(newEntry)

    # save the reviewList to the file
    writeFile(reviewList, reviewFile)
    return render_template('index1.html', reviewList=reviewList)
# ******************************************************************#

# ************* ROOM BOOKING*********************************************#
# Reading, writing and filtering a CSV file
# This was adapted from a post from user Peilonrayz on Jul 2 2015 at 17:43
# to codereview.stackexchange.com
# forum here:
# https://codereview.stackexchange.com/questions/95511/reading-writing-and-filtering-a-csv-file


# Room booking form
@app.route('/addBook', methods=['POST'])
def addBook():
	# read the bookingList from file
	bookingFile = 'static/bookingList.csv'
	bookingList = readFile(bookingFile)

	# add the new entry
	aDate = request.form[('aDate')]
	dDate = request.form[('dDate')]
	room = request.form[('room')]
	bName = request.form[('bName')]
	email = request.form[('email')]
	conf = "unconfirmed"

	newBooking = [aDate, dDate, room, bName, email, conf]
	bookingList.append(newBooking)

	# save the reviewList to the file
	writeFile(bookingList, bookingFile)

	# read and filter the confirmed bookings
	with open(bookingFile) as csv_file:
		reader = csv.reader(csv_file, delimiter=',')
		a = list()
		for row in reader:
			for index in range(len(row)):
				if (row[index] == 'confirmed'):
					a.append(row)
	bookList = a

	return render_template('booking.html', bookingList=bookingList, bookList=bookList)


# Booked rooms list
@app.route('/addBook', methods=['GET'])
def booking():
	# reads and filters bookingList csv file for confirmed bookings
	bookingFile = 'static/bookingList.csv'
	with open(bookingFile) as csv_file:
		reader = csv.reader(csv_file, delimiter=',')
		a = list()
		for row in reader:
			for index in range(len(row)):
				if (row[index] == 'confirmed'):
					# adds filtered rows to new list
					a.append(row)
	bookList = a
	return render_template('booking.html', bookList=bookList)


# Booking process check
@app.route('/bookCheck', methods=['GET', 'POST'])
def bookCheck():
	
	emailAdd = request.form[('emailA')]
	bookingFile = 'static/bookingList.csv'
	
	# read and filter the confirmed bookings
	with open(bookingFile) as csv_file:
		reader = csv.reader(csv_file, delimiter=',')
		a = list()
		for row in reader:
			for index in range(len(row)):
				if (row[index] == 'confirmed'):
					a.append(row)
	bookList = a
	
	# read and filter csv file and sets appropriate text output
	with open(bookingFile) as csv_file:
		reader = csv.reader(csv_file, delimiter=',')
		for row in reader:
			for index in range(len(row)):
				if (row[index] == emailAdd)and(row[index+1] == 'confirmed'):
					outList = [row]
					return render_template('booking.html', outList=outList, bookList=bookList)
				elif (row[index] == emailAdd):
					srr = 'Sorry, your booking is still unconfirmed'
					return render_template('booking.html', srr=srr, bookList=bookList)

# ***************************************************************************#

# ************* LOCAL ATTRACTIONS *************************#


@app.route('/local', methods=['GET'])
def local():
	return render_template('localAttractions.html')
# *********************************************************#


def readFile(aFile):
	# read in aFile 
	with open(aFile, 'r') as inFile:
		reader = csv.reader(inFile)
		reviewList = [row for row in reader]
	return reviewList


def writeFile(aList, aFile):
	# write aList to aFile
	with open(aFile, 'w') as outFile:
		writer = csv.writer(outFile)
		writer.writerows(aList)
	return

if __name__ == '__main__':
	app.run(debug=True)
