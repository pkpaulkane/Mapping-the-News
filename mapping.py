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
    sql = "SELECT Location.LocationName, Articles.URL, Articles.Title, Articles.PrimaryID FROM Articles, Location WHERE Articles.PrimaryID = %d and Location.articleID = Articles.ID" % primary_id
    mycursor.execute(sql)
    place = []
    url = []
    title = ""
    artID = []

    for result in mycursor.fetchall():
        # note: ignore duplicates
        if not result[0] in place:
            place.append( result[0] ) 
            url.append( result[1] )
            title = result[2]
            artID.append(result[3])

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

    return render_template('map.html', PrimaryID = primary_id, title = title, url = url, lat = lat, lon = lon, place = place, artID = artID)


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

    artTitle = []  
    artID = []
    
    mycursor = connection.cursor()
    mycursor.execute("SELECT Articles.Title, Articles.PrimaryID FROM Similarity inner join Articles on Articles.PrimaryID  = Similarity.Article1 WHERE Similarity.ID = %d" % primary_id)
    
    myresult = mycursor.fetchall() 

    for row in myresult: 
        artTitle.append(row[0])
        artID.append(row[1])      

    artTitle1 = []  
    artID1 = []
    
    mycursor = connection.cursor()
    mycursor.execute("SELECT Articles.Title, Articles.PrimaryID FROM Similarity inner join Articles on Articles.PrimaryID  = Similarity.Article2 WHERE Similarity.ID = %d" % primary_id)
    
    myresult1 = mycursor.fetchall() 

    for row1 in myresult1: 
        artTitle1.append(row1[0])
        artID1.append(row1[1])   

    artTitle2 = []  
    artID2 = []
    
    mycursor = connection.cursor()
    mycursor.execute("SELECT Articles.Title, Articles.PrimaryID FROM Similarity inner join Articles on Articles.PrimaryID  = Similarity.Article3 WHERE Similarity.ID = %d" % primary_id)
    
    myresult2 = mycursor.fetchall() 

    for row2 in myresult2: 
        artTitle2.append(row2[0])
        artID2.append(row2[1])    

    artTitle3 = []  
    artID3 = []
    
    mycursor = connection.cursor()
    mycursor.execute("SELECT Articles.Title, Articles.PrimaryID FROM Similarity inner join Articles on Articles.PrimaryID  = Similarity.Article4 WHERE Similarity.ID = %d" % primary_id)
    
    myresult3 = mycursor.fetchall() 

    for row3 in myresult3: 
        artTitle3.append(row3[0])
        artID3.append(row3[1])  

    artTitle4 = []  
    artID4 = []
    
    mycursor = connection.cursor()
    mycursor.execute("SELECT Articles.Title, Articles.PrimaryID FROM Similarity inner join Articles on Articles.PrimaryID  = Similarity.Article5 WHERE Similarity.ID = %d" % primary_id)
    
    myresult4 = mycursor.fetchall() 

    for row4 in myresult4: 
        artTitle4.append(row4[0])
        artID4.append(row4[1])  

    return render_template('related.html', artTitle = artTitle, artID = artID, artTitle1 = artTitle1, artID1 = artID1, artTitle2 = artTitle2, artID2 = artID2, artTitle3 = artTitle3, artID3 = artID3, artTitle4 = artTitle4, artID4 = artID4)

@app.route('/country')
def country():

        # note: check URL parameter "id"
    str_id = request.args.get("Lat", default = "0")
    str_id1 = request.args.get("Long", default = "0")
    lat = float(str_id)
    long = float(str_id1)

    coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=25e9dfb148734f&lat=%f&lon=%f&format=json" %(lat, long)) 
    print(coordinates1)
    with urllib.request.urlopen(coordinates1) as url:
        data = json.loads(url.read().decode('utf-8'))

    country = (data['address']['country'])

    mycursor = connection.cursor()
    
    sql = ("SELECT distinct Location.LocationName, Articles.URL, Articles.Title, Articles.PrimaryID FROM Articles inner join Location on Location.LocationID = Articles.PrimaryID WHERE Location.LocationName = '%s'" % country)
    print(sql)
    mycursor.execute(sql)
    
    primaryID = []
    articlesTitle = []
    articlesURL = []

    for result in mycursor.fetchall():
        primaryID.append(result[3])
        articlesTitle.append( result[2] ) 
        articlesURL.append( result[1] )

    print(primaryID, articlesTitle)    
    
    return render_template('country.html', articlesTitle = articlesTitle, articlesURL = articlesURL, primaryID = primaryID)

@app.route('/rank')
def rank():
        
    str_id = request.args.get("Location", default = "0")
    #place = float(str_id)

    country = []
    articlesTitle = []



    mycursor = connection.cursor()

    mycursor.execute("SELECT Location.LocationName, count(Location.LocationName) From Location group by Location.LocationName order by count(Location.LocationName) desc")
    myresult = mycursor.fetchall() 

    for row in myresult: 
        country.append(row[0])
    
    #print(country)

    mycursor = connection.cursor()
    mycursor.execute("SELECT Articles.Title, Articles.PrimaryID FROM Articles inner join Location on Location.LocationID = Articles.PrimaryID WHERE Location.LocationName = '%s'" % str_id)
    
    for result in mycursor.fetchall():
        articlesTitle.append( result[0]) 

    return render_template('rank.html', country = country, articlesTitle = articlesTitle)

@app.route('/details')
def details():
        
    str_id = request.args.get("Location", default = "0")
    #place = float(str_id)

    articlesTitle = []
    primaryID = []

    mycursor = connection.cursor()
    mycursor.execute("SELECT distinct Articles.Title, Articles.PrimaryID FROM Articles inner join Location on Location.LocationID = Articles.PrimaryID WHERE Location.LocationName = '%s'" % str_id)
    
    for result in mycursor.fetchall():
        articlesTitle.append( result[0]) 
        primaryID.append( result[1])

    sport = 0
    politics = 0
    business = 0
    entertainment = 0
    tech = 0


    mycursor = connection.cursor()
    mycursor.execute("SELECT distinct COUNT(categories.labels), categories.labels, Location.LocationName from Articles inner join categories on Articles.PrimaryID = categories.ID inner join Location on Location.LocationID = Articles.PrimaryID  Where Location.LocationName = '%s' group by categories.labels" % str_id)

    for result in mycursor.fetchall():
        if(result[1] == 'politics'):
            politics += float(result[0])
        
        if(result[1] == 'sport'):
            sport += float(result[0])
        
        if(result[1] == 'business'):
            business += float(result[0])
       
        if(result[1] == 'entertainment'):
            entertainment += float(result[0])
        
        if(result[1] == 'tech'):
            tech += float(result[0])
        

    #print(politics)
    #print(sport)
    #print(business)
    #print(entertainment)
    #print(tech)

    return render_template('details.html', articlesTitle = articlesTitle, primaryID = primaryID, politics = politics, sport = sport, business= business, entertainment = entertainment, tech = tech, str_id = str_id)


if __name__ == '__main__':
   app.run(debug = True,port=8080)
