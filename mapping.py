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

# Connecting to SQL database
connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Saxophone10",
  database="Mapping",
  auth_plugin="mysql_native_password"
)

print(connection)

# parameter for map
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
    
    # if no locations in articles
    if not place:
        mycursor = connection.cursor()
        sql = "SELECT Articles.URL, Articles.Title, Articles.PrimaryID FROM Articles WHERE Articles.PrimaryID = %d" % primary_id
        mycursor.execute(sql)
        url = []
        title = ""
        artID = []
        
        for result in mycursor.fetchall():
            # note: ignore duplicates
            if not result[0] in place:
                url.append( result[0] )
                title = (result[1])
                artID.append(result[2])

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

# parameter for home page
@app.route('/home')
def home():

    # declaring variables
    title = []
    primaryID = []  
    url = []
    labels = []

    mycursor = connection.cursor()
    
    # fetching all articles with their ID, URL and category label
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

# parameter for related page
@app.route('/related')
def related():

    # check the URL parameter 'ID'
    str_id = request.args.get("ID", default = "0")
    primary_id = int(str_id)

    # declaring variables
    artTitle = []  
    artID = []
    
    # fetching rank 1 of similar articles  
    mycursor = connection.cursor()
    mycursor.execute("SELECT Articles.Title, Articles.PrimaryID FROM Similarity inner join Articles on Articles.PrimaryID  = Similarity.Article1 WHERE Similarity.ID = %d" % primary_id)
    
    myresult = mycursor.fetchall() 

    for row in myresult: 
        artTitle.append(row[0])
        artID.append(row[1])      

    artTitle1 = []  
    artID1 = []
    
    # fetching rank 2 of similar articles  
    mycursor = connection.cursor()
    mycursor.execute("SELECT Articles.Title, Articles.PrimaryID FROM Similarity inner join Articles on Articles.PrimaryID  = Similarity.Article2 WHERE Similarity.ID = %d" % primary_id)
    
    myresult1 = mycursor.fetchall() 

    for row1 in myresult1: 
        artTitle1.append(row1[0])
        artID1.append(row1[1])   

    artTitle2 = []  
    artID2 = []
    
    # fetching rank 3 of similar articles  
    mycursor = connection.cursor()
    mycursor.execute("SELECT Articles.Title, Articles.PrimaryID FROM Similarity inner join Articles on Articles.PrimaryID  = Similarity.Article3 WHERE Similarity.ID = %d" % primary_id)
    
    myresult2 = mycursor.fetchall() 

    for row2 in myresult2: 
        artTitle2.append(row2[0])
        artID2.append(row2[1])    

    artTitle3 = []  
    artID3 = []
    
    # fetching rank 4 of similar articles  
    mycursor = connection.cursor()
    mycursor.execute("SELECT Articles.Title, Articles.PrimaryID FROM Similarity inner join Articles on Articles.PrimaryID  = Similarity.Article4 WHERE Similarity.ID = %d" % primary_id)
    
    myresult3 = mycursor.fetchall() 

    for row3 in myresult3: 
        artTitle3.append(row3[0])
        artID3.append(row3[1])  

    artTitle4 = []  
    artID4 = []
    
    # fetching rank 5 of similar articles  
    mycursor = connection.cursor()
    mycursor.execute("SELECT Articles.Title, Articles.PrimaryID FROM Similarity inner join Articles on Articles.PrimaryID  = Similarity.Article5 WHERE Similarity.ID = %d" % primary_id)
    
    myresult4 = mycursor.fetchall() 

    for row4 in myresult4: 
        artTitle4.append(row4[0])
        artID4.append(row4[1])  

    return render_template('related.html', artTitle = artTitle, artID = artID, artTitle1 = artTitle1, artID1 = artID1, artTitle2 = artTitle2, artID2 = artID2, artTitle3 = artTitle3, artID3 = artID3, artTitle4 = artTitle4, artID4 = artID4)

# parameter for first country page
@app.route('/country')
def country():

    # note: check URL parameter "Lat" and "Long"
    str_id = request.args.get("Lat", default = "0")
    str_id1 = request.args.get("Long", default = "0")

    lat = float(str_id)
    long = float(str_id1)

    # using LocationIQ to get country name using lat and long coordinates
    coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=25e9dfb148734f&lat=%f&lon=%f&format=json" %(lat, long)) 
    print(coordinates1)
    with urllib.request.urlopen(coordinates1) as url:
        data = json.loads(url.read().decode('utf-8'))

    country = (data['address']['country'])
    print(country)

    mycursor = connection.cursor()
    
    # fetching articles with their URL, title, ID and county
    sql = ("SELECT distinct Coordinates.Country, Articles.URL, Articles.Title, Articles.PrimaryID FROM Articles inner join Location on Location.LocationID = Articles.PrimaryID inner join Coordinates on Location.LocationName = Coordinates.Place WHERE Coordinates.Country = '%s' order by Articles.Title ASC" % country)
    print(sql)
    mycursor.execute(sql)
    
    primaryID = []
    articlesTitle = []
    articlesURL = []

    for result in mycursor.fetchall():
        primaryID.append(result[3])
        articlesTitle.append( result[2] ) 
        articlesURL.append( result[1] )  
    
    return render_template('country.html', articlesTitle = articlesTitle, articlesURL = articlesURL, primaryID = primaryID, country = country)

# parameter for rank page
@app.route('/rank')
def rank():

    return render_template('rank.html')

# parameter for calendar page
@app.route('/calendar')
def calendar():
    
    # note: check URL parameter "date" and "category"
    date_id = request.args.get("date", default = "")
    category_id = request.args.get("category", default = "")
    

    mycursor = connection.cursor()

    # fetching distinct place names
    sql = "SELECT Distinct Location.LocationName FROM  Location, Articles inner join categories on Articles.PrimaryID = categories.ID WHERE Articles.Date = '%s' and Location.articleID = Articles.ID and categories.labels = '%s'" % (date_id, category_id)
    print(sql)
    mycursor.execute(sql)
    
    place = []

    for result in mycursor.fetchall():
        # note: ignore duplicates
        if not result[0] in place:
            place.append( result[0] ) 

    print(place)

    # Get the Coordinates next
    lat = []
    lon = []
    for placename in place:
        sql = "SELECT Latitude, Longitude FROM Coordinates WHERE Place='%s'" % placename
        mycursor.execute(sql)
        for result in mycursor.fetchall():
            lat.append(result[0])
            lon.append(result[1])

    return render_template('calendar.html',  lat = lat, lon = lon, place = place, date_id = date_id, category_id = category_id)

# parameter for click page
@app.route('/click')
def click():
    
    return render_template('click.html')

# parameter for the second country page
@app.route('/country2')
def country2():

    # note: check URL parameter "Country"
    str_id = request.args.get("Country", default = " ")
    
    mycursor = connection.cursor()
    
    # fetching distinct location based on articles with their URL and PrimaryID
    sql = ("SELECT distinct Location.LocationName, Articles.URL, Articles.Title, Articles.PrimaryID FROM Articles inner join Location on Location.LocationID = Articles.PrimaryID inner join Coordinates on Location.LocationName = Coordinates.Place WHERE Location.LocationName = '%s' order by Articles.Title ASC" % str_id)
    print(sql)
    mycursor.execute(sql)
    
    primaryID = []
    articlesTitle = []
    articlesURL = []

    for result in mycursor.fetchall():
        primaryID.append(result[3])
        articlesTitle.append( result[2] ) 
        articlesURL.append( result[1] )
  
    return render_template('country2.html', articlesTitle = articlesTitle, articlesURL = articlesURL, primaryID = primaryID, str_id = str_id)

# parameter for third country page
@app.route('/country3')
def country3():

    # note: check URL parameter "Country" and "Date" and "Category"
    str_id = request.args.get("Country", default = " ")
    date_id = request.args.get("Date", default = " ")
    category_id = request.args.get("Category", default = " ")
    
    mycursor = connection.cursor()
    
    # fetching distinct location based on articles with their URL and PrimaryID
    sql = ("SELECT distinct Location.LocationName, Articles.URL, Articles.Title, Articles.PrimaryID FROM Articles inner join Location on Location.LocationID = Articles.PrimaryID inner join Coordinates on Location.LocationName = Coordinates.Place inner join categories on Articles.PrimaryID = categories.ID WHERE Location.LocationName = '%s' and Articles.Date = '%s' and categories.labels = '%s' order by Articles.Title ASC" % (str_id, date_id, category_id))
    print(sql)
    mycursor.execute(sql)
    
    primaryID = []
    articlesTitle = []
    articlesURL = []

    for result in mycursor.fetchall():
        primaryID.append(result[3])
        articlesTitle.append( result[2] ) 
        articlesURL.append( result[1] )
  
    return render_template('country2.html', articlesTitle = articlesTitle, articlesURL = articlesURL, primaryID = primaryID, str_id = str_id)

if __name__ == '__main__':
   app.run(debug = True,port=8080)
