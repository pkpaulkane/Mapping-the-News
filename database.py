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
import pickle
from flask import Flask
from flask import render_template
import heapq
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

filename = "errorLog.csv"
# opening the file with w+ mode truncates the file
f = open(filename, "w+")
f.close()

list = []

with open('guardian-2017.jsonl', 'r') as f:
    for item in json_lines.reader(f):
        content = item
        count += 1
        body = (item['fields']['bodyText'])
        title = (content['webTitle'])
        sectionID = content['sectionId']
        date = content['webPublicationDate'][:10]
        print(count)

        sql_insert_query = """ INSERT INTO `Articles`
                          (`ID`, `BodyText`, `URL`, `Title`, `PrimaryID`, `sectionID`, `Date`) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        cursor = connection.cursor()
        cursor.execute(sql_insert_query, (content['id'], content['fields']['bodyText'],content['webUrl'], content['webTitle'], count, sectionID, date ))
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
                              #sentence1 = 'https://us1.locationiq.com/v1/search.php?key=25e9dfb148734f&q=PLACE&format=json'
                              #sentence1 = re.sub(r'\bPLACE\b', places, entity1)



                              #time.sleep(0.75)
                              #with urllib.request.urlopen(sentence1) as url:
                                #data = json.loads(url.read().decode('utf-8'))
                                  
                                #latitude = data[0]['lat']
                                #longitude = (data[0]['lon'])
                                sql_insert_query = """ INSERT INTO `Location`
                                              (`Count`, `articleID`,`LocationName`, `LocationID`) VALUES (%s, %s, %s, %s)"""

                                cursor = connection.cursor()
                                cursor.execute(sql_insert_query, (counter, content['id'], entity1.text, count))
                                counter += 1
                                connection.commit()
                    
        #if count == 100:
          #break 
#print(list)
mycursor = connection.cursor()


mycursor = connection.cursor()

mycursor.execute("SELECT COUNT(DISTINCT LocationName) FROM Location")
myresult = mycursor.fetchall()[0]

counting = 0

for x in myresult:
  total = x

for z in range(total):
  #print(z)
  mycursor = connection.cursor()

  mycursor.execute("SELECT DISTINCT LocationName FROM Location")
  result = mycursor.fetchall()[z]

  for places in result:
    locations = places

   # for word in list:
    #    if word in locations:
     #       list.remove(locations)
                
            #for words in list:
             #   if words in locations:
              #      list.remove(locations)
            

      
    counting += 1

    if counting < 5000:  
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=25e9dfb148734f&q=PLACE&format=json'

    elif counting >= 5000 and counting < 10000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=1ec81b8a7454a2&q=PLACE&format=json'
    
    elif counting >= 10000 and counting < 15000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=8f244b5da51d53&q=PLACE&format=json'
    
    elif counting >= 15000 and counting < 20000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=ac5acb030a42bc&q=PLACE&format=json'
    
    elif counting >= 20000 and counting < 25000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=b88418f9a94ae5&q=PLACE&format=json'
    
    elif counting >= 25000 and counting < 30000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=b3c36817286528&q=PLACE&format=json'
    
    elif counting >= 30000 and counting < 35000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=52cca27b8970d5&q=PLACE&format=json'
    
    elif counting >= 35000 and counting < 40000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=ce4ac18e483d55&q=PLACE&format=json'
   
    elif counting >= 40000 and counting < 45000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=97f5412cd01141&q=PLACE&format=json'
    
    elif counting >= 45000 and counting < 50000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=33958a39a49693&q=PLACE&format=json'
    
    elif counting >= 50000 and counting < 55000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=7833ac9400b3cf&q=PLACE&format=json'
    
    elif counting >= 55000 and counting < 60000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=13584d5082f9aa&q=PLACE&format=json'
    
    elif counting >= 60000 and counting < 65000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=375f923c63f449&q=PLACE&format=json'
    
    elif counting >= 65000 and counting < 70000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=ed454ec6362a9c&q=PLACE&format=json'
    
    elif counting >= 70000 and counting < 75000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=c2f90a6d00f76d&q=PLACE&format=json'
    
    elif counting >= 75000 and counting < 80000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=de905daded04e6&q=PLACE&format=json'
    
    elif counting >= 80000 and counting < 85000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=602f7c9167be51&q=PLACE&format=json'
    
    elif counting >= 85000 and counting < 90000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=02fcd6939613b5&q=PLACE&format=json'
    
    elif counting >= 90000 and counting < 95000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=cbd5f5d9b42a5c&q=PLACE&format=json'
    
    elif counting >= 95000 and counting < 100000:
      sentence1 = 'https://us1.locationiq.com/v1/search.php?key=739aeeb96829af&q=PLACE&format=json'
    
    if not places.strip():
      places = 'Ireland'
    
    sentence1 = re.sub(r'\bPLACE\b', places, sentence1)
    print(counting)
    print(places)
    print(sentence1)
    
    


    time.sleep(0.75)
    with urllib.request.urlopen(sentence1) as url:
      data = json.loads(url.read().decode('utf-8'))
        
      latitude = data[0]['lat']
      longitude = (data[0]['lon'])
      lat = float(latitude)
      long = float(longitude)
      
      if counting < 5000:  
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=25e9dfb148734f&lat=%f&lon=%f&format=json" %(lat, long))
  
      elif counting >= 5000 and counting < 10000:
        coordinates1 = '("https://eu1.locationiq.com/v1/reverse.php?key=1ec81b8a7454a2&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 10000 and counting < 15000:
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=8f244b5da51d53&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 15000 and counting < 20000:
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=ac5acb030a42bc&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 20000 and counting < 25000:
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=b88418f9a94ae5&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 25000 and counting < 30000:
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=b3c36817286528&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 30000 and counting < 35000:
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=52cca27b8970d5&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 35000 and counting < 40000:
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=ce4ac18e483d55&lat=%f&lon=%f&format=json" %(lat, long))
    
      elif counting >= 40000 and counting < 45000:
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=97f5412cd01141&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 45000 and counting < 50000:
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=33958a39a49693&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 50000 and counting < 55000:
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=7833ac9400b3cf&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 55000 and counting < 60000:
        coordinates1 =  ("https://eu1.locationiq.com/v1/reverse.php?key=13584d5082f9aa&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 60000 and counting < 65000:
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=375f923c63f449&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 65000 and counting < 70000:
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=ed454ec6362a9c&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 70000 and counting < 75000:
        coordinates1 =  ("https://eu1.locationiq.com/v1/reverse.php?key=c2f90a6d00f76d&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 75000 and counting < 80000:
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=de905daded04e6&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 80000 and counting < 85000:
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=602f7c9167be51&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 85000 and counting < 90000:
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=02fcd6939613b5&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 90000 and counting < 95000:
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=cbd5f5d9b42a5c&lat=%f&lon=%f&format=json" %(lat, long))
      
      elif counting >= 95000 and counting < 100000:
        coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=739aeeb96829af&lat=%f&lon=%f&format=json" %(lat, long))
      
      #print(coordinates1)
      with urllib.request.urlopen(coordinates1) as url:
          data = json.loads(url.read().decode('utf-8'))

      if('country' in data['address']):
        country = (data['address']['country'])
        
      elif('city' in data['address']): 
          country = (data['address']['city'])

      else:
        country = " "
      
      print(country)
    
      sql_insert_query = """ INSERT INTO `Coordinates`
                    (`Counter`, `Place`, `Longitude`, `Latitude`, `Country`) VALUES (%s, %s, %s, %s, %s)"""

      cursor = connection.cursor()
      cursor.execute(sql_insert_query, (counting, places, latitude, longitude, country))
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

with open('errorLog.csv', "w") as f:
    writer = csv.writer(f)
    for row in removeDuplicates:
        writer.writerow([row])