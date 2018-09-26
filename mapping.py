from collections import Counter
import json_lines
import json
import spacy
import nltk

with open('sample1.jsonl', 'r') as f:
    for item in json_lines.reader(f):
        content = (item['fields']['bodyText'])

        #print(content)

        nlp = spacy.load('en_core_web_sm')

        text = content

        doc = nlp(text)

        for entity in doc.ents:
            if entity.label_ in ('GPE'):
                print(entity.text, entity.label_ )

        tokens = nltk.word_tokenize(text)

        tagged = nltk.pos_tag(tokens)

        entities = nltk.chunk.ne_chunk(tagged)

        for word, tag in tagged: 
            if tag in ('NNP'):
                #print((word, tag)) 

                document = nlp(word)

                for entity1 in document.ents:
                     if entity1.label_ in ('GPE'):
                         print(entity1.text)
                



       


