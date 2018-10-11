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

        doc = nlp(text)

        tokens = nltk.word_tokenize(text)

        tagged = nltk.pos_tag(tokens)

        entities = nltk.chunk.ne_chunk(tagged)

        for word, tag in tagged: 
            if tag in ('NNP'):
                #print((word, tag)) 

                document = nlp(word)

                for entity1 in document.ents:
                     if entity1.label_ in ('GPE'):
                          #print(id['id'], entity1.text)
                
                          counts = int(str(count) + str(counter))

                          sql_insert_query = """ INSERT INTO `Location`
                                              (`Count`, `articleID`,`LocationName`) VALUES (%s, %s, %s)"""

                          cursor = connection.cursor()
                          cursor.execute(sql_insert_query, (counter, content['id'], entity1.text))
                          counter += 1
                          connection.commit()
                    
        if count == 10:
          break 

mycursor = connection.cursor()

mycursor.execute("SELECT COUNT(DISTINCT LocationName) FROM Location")
myresult = mycursor.fetchall()[0]

counting = 0

for x in myresult:
  print(x)

for z in range(x):
  #print(z)
  mycursor = connection.cursor()

  mycursor.execute("SELECT DISTINCT LocationName FROM Location")
  result = mycursor.fetchall()[z]

  for x in result:
    print(x)
      
    counting += 1
      
    countID = int(str(counting) + str(counts))

    sentence1 = 'https://us1.locationiq.com/v1/search.php?key=25e9dfb148734f&q=PLACE&format=json'
    sentence1 = re.sub(r'\bPLACE\b', x, sentence1)

    time.sleep(0.75)
    with urllib.request.urlopen(sentence1) as url:
      data = json.loads(url.read().decode('utf-8'))
        
      latitude = data[0]['lat']
      longitude = (data[0]['lon'])

      sql_insert_query = """ INSERT INTO `Coordinates`
                    (`Counter`, `Place`, `Longitude`, `Latitude`) VALUES (%s, %s, %s, %s)"""

      cursor = connection.cursor()
      cursor.execute(sql_insert_query, (counting, x, latitude, longitude))
      connection.commit()
                  
                             
                         

                
                



       


