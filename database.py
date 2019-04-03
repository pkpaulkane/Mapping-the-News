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
from nltk.corpus import wordnet as wn
import pandas as pd
import numpy
import numpy as np

app = Flask(__name__)

# connecting to MySQL
connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Saxophone10",
  database="Mapping",
  auth_plugin="mysql_native_password"
)

print(connection)

# setting counter values which will be used for ID's later on
counter = 0
count = 0

# loading the spaCy library with English
nlp = spacy.load('en_core_web_sm')

# delete statements used to fill up tables if something in them
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

#
filename = "errorLog.csv"

# opening the errorlog with w+ mode truncates the file
f = open(filename, "w+")
f.close()

list = []

df = pd.read_csv('Articles.csv',sep=';',header=0, encoding = 'utf8')

## Pre-processing used for the tokens 
def convert_hyphens(series):
    """
    Takes a string of text and returns a string of text with hyphens replaced by underscores.
    We do this so words like "e-mail", "wi-fi", etc. are kept together.
    """
    return series.replace("-", "_")


def tokenize(series):
    """
    Takes a string of text and returns a list of string tokens.
    """
    # Pattern matches one or more alphanumeric characters (or underscores).
    TOKENIZER_REGEX = r'\w+'
    tokenizer = nltk.tokenize.RegexpTokenizer(TOKENIZER_REGEX)  
    return tokenizer.tokenize(series)


def decapitalize(series):
    """
    Takes a list of tokens and returns a list of tokens, with every token in lowercase form.
    """
    # Map the string to-lowercase method to every value in the series.
    return [word.lower() for word in series]
    

def remove_special_chars(series):
    """
    Takes a list of tokens and returns that list, without special characters.
    """    
    words_to_remove = set(["", "_"])
    return [word.replace("_", "") for word in series if word not in words_to_remove]

def remove_numbers(series):
    """
    Takes a list of tokens and returns a list of tokens that do not consist solely of numeric characters.
    For example, "3" is removed, but not "3G" or "Three".
    """
    return [word for word in series if not word.isnumeric()]

def remove_punctuation(series):
    """ 
    Takes a list of tokens and returns a list of tokens, with any punctuation stripped.
    """
    results = []
    
    for word in series:
        new_word = "".join(character for character in word if character not in string.punctuation)
        
        if new_word is not "":
            results.append(new_word)
    
    return results


def remove_stop_words(series):
    """
    Takes a list of tokens and returns a list of those tokens that are not contained 
    in the stop words list.
    """
    return [word for word in series if word not in get_stop_words()]
    
    
def lemmatize(series):   

    lemmatizer = nltk.stem.WordNetLemmatizer()
    
    lemmatized_words = []
    for word, tag in nltk.pos_tag(series):
        wordnet_tag = pos_to_wordnet_tag(tag)
        lemmatized_words.extend([lemmatizer.lemmatize(word, wordnet_tag)])
        
    return lemmatized_words


def normalize_text(series, keep_stop_words=False, lemmatization=True):
    """ 
    Takes a pandas Series object and returns a list of tokens for that series.
    """
    newseries = (series.apply(convert_hyphens)
                  .apply(tokenize)
                  .apply(remove_special_chars)
                  .apply(decapitalize)
                  .apply(remove_numbers))
    
    if lemmatization:
        newseries = newseries.apply(lemmatize)
    
    if not keep_stop_words:
        newseries = newseries.apply(remove_stop_words)

    return newseries

# setting the content as the BodyText and then normalizing it
corpus_content = df['BodyText']
corpus_content = normalize_text(corpus_content, keep_stop_words=True, lemmatization=False)


# opening the jsonl file for extracting article information
with open('guardian-2017.jsonl', 'r') as f:
    for item in json_lines.reader(f):
        
        #count used as the primaryID for each article
        count += 1
        
        #extracting the relevant fields
        content = item
        body = (item['fields']['bodyText'])
        title = (content['webTitle'])
        sectionID = content['sectionId']
        date = content['webPublicationDate'][:10]
        
        #used for debugging purposes
        print(count)
		
		#inserting the data in MySQL database
        sql_insert_query = """ INSERT INTO `Articles`
                          (`ID`, `BodyText`, `URL`, `Title`, `PrimaryID`, `sectionID`, `Date`) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        cursor = connection.cursor()
        cursor.execute(sql_insert_query, (content['id'], content['fields']['bodyText'],content['webUrl'], content['webTitle'], count, sectionID, date ))
        connection.commit()
		
		#applying spaCy NLP to tokenize text
        text = body
        text = re.sub(r'[^\w\s]',' ',text)
        doc = nlp(text)

		#nltk tokenizing text
        tokens = nltk.word_tokenize(text)

		#nltk taggings token
        tagged = nltk.pos_tag(tokens)
		
		#dividing the entities
        entities = nltk.chunk.ne_chunk(tagged)
                
        #for any entity with the tag 'GPE'
        for entity1 in doc.ents:
                if entity1.label_ in ('GPE'):
                    
                    #add entity to list
                    list.append(entity1.text) 
                    
                    #run entity through world database 
                    with open('MappingData.csv', 'r') as ff:
                        reader2 = csv.reader(ff, delimiter=',')
                        for row in reader2:
                            if(entity1.text == row[0]):
                            	#insert data into location database
                                sql_insert_query = """ INSERT INTO `Location`
                                              (`Count`, `articleID`,`LocationName`, `LocationID`) VALUES (%s, %s, %s, %s)"""

                                cursor = connection.cursor()
                                cursor.execute(sql_insert_query, (counter, content['id'], entity1.text, count))
                                counter += 1
                                connection.commit()
                    
mycursor = connection.cursor()



#fetching the number of distinct location names
mycursor.execute("SELECT COUNT(DISTINCT LocationName) FROM Location")
myresult = mycursor.fetchall()[0]

counting = 0

for x in myresult:
  total = x

for z in range(total):
  mycursor = connection.cursor()

	# getting all the distinct place names
  mycursor.execute("SELECT DISTINCT LocationName FROM Location")
  result = mycursor.fetchall()[z]

  for places in result:
    locations = places
    counting += 1
 
    sentence1 = 'https://us1.locationiq.com/v1/search.php?key=25e9dfb148734f&q=PLACE&format=json'

    if not places.strip():
      places = 'Neverland'
    
    #getting locations for each of the different place names with LocationIQ
    sentence1 = re.sub(r'\bPLACE\b', places, sentence1)
    
    # for all of the article
    for article in range(82677):
	
        length = (len(corpus_content[article]))
        
        ID = []
        Location = []
        list = []
        mycursor = connection.cursor()
        
        #Fetching the location names
        mycursor.execute("SELECT DISTINCT LocationID, LocationName FROM Location")
        for result in mycursor.fetchall():

            if result[0] == article:
                list.append(result[1])    
        values = []

        # calculating the total WordNet values for each place
        for j in range (len(list)):
            total = 0
            for i in range(length):
                total += (find_distance_wordnet(list[j], corpus_content[article][i]))
            values.append(total)
        
            #getting the max values place
            max_value = max(values)
            place = values.index(max_value)
    
    #timer to prevent number of requests exceeding limit
    time.sleep(0.75)
    with urllib.request.urlopen(sentence1) as url:
      data = json.loads(url.read().decode('utf-8'))
      
      #setting coordinates from json  
      latitude = data[0]['lat']
      longitude = (data[0]['lon'])
      lat = float(latitude)
      long = float(longitude)
      
      #getting location details based on coordinates
      coordinates1 = ("https://eu1.locationiq.com/v1/reverse.php?key=25e9dfb148734f&lat=%f&lon=%f&format=json" %(lat, long))
  
      with urllib.request.urlopen(coordinates1) as url:
          data = json.loads(url.read().decode('utf-8'))
		
		#get country name if it exists
      if('country' in data['address']):
        country = (data['address']['country'])
        
        #get city name if there's no country
      elif('city' in data['address']): 
          country = (data['address']['city'])

		#otherwise blank
      else:
        country = " "
      
      print(country)
    
    	#insert place name and coordinates into MySQL database
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

# adding data to error log to
with open('errorLog.csv', "w") as f:
    writer = csv.writer(f)
    for row in removeDuplicates:
        writer.writerow([row])

#defining the wordNet similarity 
def find_distance_wordnet(word1,word2):
    from nltk.corpus import wordnet as wn
    _similarity = 0
    for eachsyn in wn.synsets(word1):
        for eachsyn2 in wn.synsets(word2):
            path_simi = (wn.path_similarity(eachsyn,eachsyn2))
            if (path_simi != None):
                if (_similarity < path_simi):
                    _similarity = path_simi
    return _similarity  