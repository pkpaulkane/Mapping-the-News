from collections import Counter
import json_lines
import json
import spacy
import nltk
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import re
import urllib.request, json
import time 
import csv
from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Saxophone10",
  database="Mapping",
  auth_plugin="mysql_native_password"
)

print(connection)


@app.route('/articles/')
def articles():

    title = []
    primaryID = []  
    url = []

    mycursor = connection.cursor()
    mycursor.execute("SELECT Distinct Title, PrimaryID, url  FROM Mapping.Articles order by Title ASC")
    myresult = mycursor.fetchall() 

    for row in myresult: 
        title.append(row[0])
        primaryID.append(row[1])
        url.append(row[2])
    return render_template('articles.html', title = title, primaryID = primaryID, url =url )
    
@app.route('/map')
def map(): 
    PrimaryID = request.args.get('PrimaryID')

    lat = []
    lon = []
    url = []
    place = []  
    title = []

    cursor = connection.cursor()
    cursor.execute("SELECT Distinct BodyText, URL, LocationName, Longitude, Latitude, PrimaryID, Title  FROM Mapping.Location INNER JOIN Mapping.Articles ON  Mapping.Articles.PrimaryID = Mapping.Location.LocationID INNER JOIN Mapping.Coordinates ON  Mapping.Coordinates.Place = Mapping.Location.LocationName  WHERE PrimaryID = " + PrimaryID)
    result = cursor.fetchall() 

    for row in result: 
        title.append(row[6])
        lat.append(row[4])
        lon.append(row[3])
        url.append(row[1])
        place.append(row[2])


    return render_template('map.html', PrimaryID = PrimaryID, title = title, url = url, lat = lat, lon = lon, place = place)

@app.route('/business/')
def business():
    return render_template('business.html')

@app.route('/entertainmemt/')
def entertainment():
    return render_template('entertainment.html')

@app.route('/politics')
def politics():

    return render_template('politics.html')

if __name__ == '__main__':
   app.run(debug = True,port=8080)
                  
                          
                         

                
                



       


