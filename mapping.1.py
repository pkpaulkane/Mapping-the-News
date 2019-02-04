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


    
@app.route('/map')
def map(): 
    # note: check URL parameter "id"
    str_id = request.args.get("PrimaryID", default = "0")
    primary_id = int(str_id)

    mycursor = connection.cursor()
    
    # Get the Locations first
    sql = "SELECT Location.LocationName, Articles.URL, Articles.Title FROM Articles, Location WHERE Articles.PrimaryID = %d and Location.articleID = Articles.ID" % primary_id
    mycursor.execute(sql)
    place = []
    url = []
    title = ""
    for result in mycursor.fetchall():
        # note: ignore duplicates
        if not result[0] in place:
            place.append( result[0] ) 
            url.append( result[1] )
            title = result[2]

    # Get the Coordinates next
    lat = []
    lon = []
    for placename in place:
        sql = "SELECT Latitude, Longitude FROM Coordinates WHERE Place='%s'" % placename
        mycursor.execute(sql)
        for result in mycursor.fetchall():
            lat.append(result[0])
            lon.append(result[1])

    # note: Just for debugging
    for i in range( len(place) ):
        print( place[i], lat[i], lon[i] )

    return render_template('map.html', PrimaryID = primary_id, title = title, url = url, lat = lat, lon = lon, place = place)


@app.route('/home')
def home():

    title = []
    primaryID = []  
    url = []
    labels = []

    mycursor = connection.cursor()
    #mycursor.execute("SELECT Distinct Articles.Title, Articles.PrimaryID, Articles.url, categories.labels FROM Articles, categories order by Articles.Title ASC")
    mycursor.execute("SELECT Articles.Title, Articles.PrimaryID, Articles.url, categories.labels FROM categories inner join Articles on Articles.PrimaryID  = categories.ID order by Articles.Title ASC")
    myresult = mycursor.fetchall() 

    for row in myresult: 
        title.append(row[0])
        primaryID.append(row[1])
        # note: create web app URL with numeric ID
        map_url = "/map?PrimaryID=%s" % row[1]
        url.append(map_url)
        labels.append(row[3])
    return render_template('home.html', title = title, primaryID = primaryID, url =url, labels = labels)

@app.route('/related')
def related():

    str_id = request.args.get("ID", default = "0")
    primary_id = int(str_id)
    
    simID = []
    artTitle = []  
    artID = []
    artURL = []

    mycursor = connection.cursor()
    mycursor.execute("SELECT Similarity.ID, Articles.Title, Articles.PrimaryID, Articles.url FROM Similarity inner join Articles on Articles.PrimaryID  = Similarity.Article1 WHERE similarity.ID = %d" % primary_id)
    #mycursor.execute("SELECT Articles.Title, Articles.PrimaryID, Articles.url, categories.labels FROM categories inner join Articles on Articles.PrimaryID  = categories.ID order by Articles.Title ASC")
    myresult = mycursor.fetchall() 

    for row in myresult: 
        simID.append(row[0])
        artTitle.append(row[1])
        artID.append(row[2])        
        art_url = "/related?ID=%s" % row[0]
        artURL.append(art_url)
        #artURL.append(row[3])
    return render_template('related.html', simID = simID, artTitle = artTitle, artID = artID, artURL = artURL)


if __name__ == '__main__':
   app.run(debug = True,port=8080)
