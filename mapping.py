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

counter = 0
count = 0
nlp = spacy.load('en_core_web_sm')

sql_delete_query = """ DELETE FROM `Articles`
                    WHERE ID IS NOT NULL"""

cursor = connection.cursor() 
cursor.execute(sql_delete_query)
connection.commit()

sql_delete_query = """ DELETE FROM `Location`
                    WHERE articleID IS NOT NULL"""

cursor = connection.cursor() 
cursor.execute(sql_delete_query)
connection.commit()

sql_delete_query = """ DELETE FROM `Coordinates`
                    WHERE Counter IS NOT NULL"""

cursor = connection.cursor() 
cursor.execute(sql_delete_query)
connection.commit()

filename = "newdata.csv"
# opening the file with w+ mode truncates the file
f = open(filename, "w+")
f.close()

list = []

with open('guardian-2017.jsonl', 'r') as f:
    for item in json_lines.reader(f):
        content = item
        count += 1
        body = (item['fields']['bodyText'])

        sql_insert_query = """ INSERT INTO `Articles`
                          (`ID`, `BodyText`, `URL`) VALUES (%s, %s, %s)"""

        cursor = connection.cursor()
        cursor.execute(sql_insert_query, (content['id'], content['fields']['bodyText'],content['webUrl'] ))
        connection.commit()

        text = body
        text = re.sub(r'[^\w\s]',' ',text)
        doc = nlp(text)

        tokens = nltk.word_tokenize(text)

        tagged = nltk.pos_tag(tokens)

        entities = nltk.chunk.ne_chunk(tagged)

        
        
        for entity1 in doc.ents:
                if entity1.label_ in ('GPE'):
                    #print(doc)
                    #print(entity1.text)
                    
                    list.append(entity1.text) 
                    
                    with open('MappingData.csv', 'r') as ff:
                        reader2 = csv.reader(ff, delimiter=',')
                        for row in reader2:
                            if(entity1.text == row[0]):
                                #print(entity1.text)
                                sql_insert_query = """ INSERT INTO `Location`
                                              (`Count`, `articleID`,`LocationName`) VALUES (%s, %s, %s)"""

                                cursor = connection.cursor()
                                cursor.execute(sql_insert_query, (counter, content['id'], entity1.text))
                                counter += 1
                                connection.commit()
                    
        if count == 2:
          break 
#print(list)

mycursor = connection.cursor()

mycursor.execute("SELECT COUNT(DISTINCT LocationName) FROM Location")
myresult = mycursor.fetchall()[0]

counting = 0

for x in myresult:
  total = x

for z in range(total):
  print(z)
  mycursor = connection.cursor()

  mycursor.execute("SELECT DISTINCT LocationName FROM Location")
  result = mycursor.fetchall()[z]

  for places in result:
    locations = places

    for word in list:
        if word in locations:
            list.remove(locations)
                
            for words in list:
                if words in locations:
                    list.remove(locations)
            

      
    counting += 1
      
    sentence1 = 'https://us1.locationiq.com/v1/search.php?key=25e9dfb148734f&q=PLACE&format=json'
    sentence1 = re.sub(r'\bPLACE\b', places, sentence1)



    time.sleep(0.75)
    with urllib.request.urlopen(sentence1) as url:
      data = json.loads(url.read().decode('utf-8'))
        
      latitude = data[0]['lat']
      longitude = (data[0]['lon'])

      sql_insert_query = """ INSERT INTO `Coordinates`
                    (`Counter`, `Place`, `Longitude`, `Latitude`) VALUES (%s, %s, %s, %s)"""

      cursor = connection.cursor()
      cursor.execute(sql_insert_query, (counting, places, latitude, longitude))
      connection.commit()

#Removing duplicates fromm list of unknown places
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 
      
# Driver Code 
removeDuplicates = Remove(list)

with open('newdata.csv', "w") as f:
    writer = csv.writer(f)
    for row in removeDuplicates:
        writer.writerow([row])

@app.route('/map')
def map(): 

    lat = []
    lon = []
    url = []
    place = []  
    mycursor = connection.cursor()
    mycursor.execute("SELECT DISTINCT Latitude, Longitude, URL, LocationName FROM Mapping.Location INNER JOIN Mapping.Articles ON  Mapping.Articles.ID = Mapping.Location.articleID INNER JOIN Mapping.Coordinates ON  Mapping.Coordinates.Place = Mapping.Location.LocationName")
    #mycursor.execute("SELECT Latitude, Longitude, Place, Counter from Coordinates")
    myresult = mycursor.fetchall() 

    for row in myresult: 
        lat.append(row[0])
        lon.append(row[1])
        url.append(row[2])
        place.append(row[3])


    return render_template('map4.html', url = url, lat = lat, lon = lon, place = place )

if __name__ == '__main__':
   app.run(debug = True,port=8080)
                  
                          
                         

                
                



       


