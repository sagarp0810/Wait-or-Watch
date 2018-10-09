import sys
import os
import re
import requests
import urllib2
import mysql.connector
import datetime
from bs4 import BeautifulSoup
from smtplib import SMTP_SSL
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def isInternetOn():
    try:
        urllib2.urlopen('https://www.google.com/', timeout=1)
        return True
    except urllib2.URLError as err: 
        return False

def monthToNum(month):
	return{
		    'Jan' : 1,
		    'Feb' : 2,
		    'Mar' : 3,
		    'Apr' : 4,
		    ' Ma' : 5,
		    'Jun' : 6,
		    'Jul' : 7,
		    'Aug' : 8,
		    'Sep' : 9, 
		    'Oct' : 10,
		    'Nov' : 11,
		    'Dec' : 12
	}[month]


def numToMonth(num):
	return{
		    1 : 'Jan',
		    2 : 'Feb',
		    3 : 'Mar',
		    4 : 'Apr',
		    5 : 'May',
		    6 : 'Jun',
		    7 : 'Jul',
		    8 : 'Aug',
		    9 : 'Sep',
		    10 : 'Oct',
		    11 : 'Nov',
		    12 : 'Dec'
	}[num]
	
def dateToNum(s):
	if len(s)==0:
		date = 0
	elif len(s)==4:
		date =  int(s)*10000 + 1232
	else:
		date = int(s[-4:len(s)])*10000
		date += monthToNum(s[-9:-6])*100
		date += int(s[0:2])
	return date	
	
def numToDate(d):
	date = d[6:8] + " " + numToMonth(int(d[4:6])) + ", " + d[0:4]
	return date

def showStatus(d):
	if d==0:
		status = "The show has finished streaming all its episodes."
	elif d==1:
		status = "The next season is confirmed, dates yet to be announced."
	elif d==2:
		status = "The next episode dates are not announced yet."
	elif d%100==32:
		status = "The next season begins in " + str(d/10000) + "."
	else:
		status = "The next episode airs on " + numToDate(str(d)) + "."
	return status

if not isInternetOn:
	print "Uh Oh! Seems that you are not connected to the Internet. Please check and try again later."
	exit()

mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  passwd = "qwerty"
)

cursor = mydb.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS sde")

mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  passwd = "qwerty",
  database = "sde"
)

cursor = mydb.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS waitorwatch (email VARCHAR(255), tv_series VARCHAR(255))")

x = datetime.date.today()
cur_date = x.year*10000 + x.month*100 + x.day

print "Welcome to Wait-or-Watch!!!\n"
print "Email address:",
email = raw_input()
print "TV Series:",
tv_series = raw_input()
print

SMTPserver = 'smtp.gmail.com'
sender = 'waitorwatch@gmail.com'
destination = email
password = "W@it0rW@tch"
body = ""
subject = "TV Series Information"

sql = "INSERT INTO waitorwatch VALUES (%s, %s)"
val = (email, tv_series)
cursor.execute(sql, val)
mydb.commit()

tv_series = [s.strip().capitalize() for s in tv_series.split(',')]

for series in tv_series:
	series.replace(" ", "+")
	date = []
	temp = 0

	wiki = "https://www.imdb.com/find?q=" + series
	page = requests.get(wiki).text
	soup = BeautifulSoup(page, 'lxml')

	search = soup.find('div', class_='findSection').table.find('tr').find('td').a
	href = search['href']
	id = href.split('/')[2]

	wiki = "https://www.imdb.com/title/" + id
	page = requests.get(wiki).text
	soup = BeautifulSoup(page, 'lxml')

	season_div = soup.find('div', class_='seasons-and-year-nav')
	season = season_div.find_all('div')[2].find('a').text
	
	rating_div = soup.find('div', class_='ratingValue')
	rating = rating_div.strong.span.text

	wiki = "https://www.imdb.com/title/" + id + "/episodes?season=" + season
	page = requests.get(wiki).text
	soup = BeautifulSoup(page, 'lxml')
	body += "TV Series name: " + series + "\n"
	body += "IMDb Rating: " + rating + "\n"
	
	for i in soup.find_all('div', class_='airdate'):
		date.append(dateToNum(i.text.strip()))
		
	for d in date:
		if date[0]==0:
			temp = 1
			break
		if d>cur_date:
			temp = d
			break
		if d==0:
			temp = 2
			break
	
	body += "Status: " + showStatus(temp) + "\n\n"
	
try:
	msg = MIMEMultipart()
	msg['From'] = sender
	msg['To'] = destination
	msg['Subject'] = subject
	msg.attach(MIMEText(body))

	conn = SMTP_SSL(SMTPserver)
	conn.set_debuglevel(False)
	conn.login(sender, password)

	try:
		conn.sendmail(sender, [destination], msg.as_string())
		print "Email sent to " + destination + " successfully!"
	finally:
		conn.quit()

except:
	print "Unable to send email! Please try again later."