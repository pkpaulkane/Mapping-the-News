import json_lines
import json
import spacy
import nltk

with open('guardian_sample.jsonl', 'r') as f:
    for item in json_lines.reader(f):
        content = (item['fields']['bodyText'])

        #print(content)

        nlp = spacy.load('en_core_web_sm')

        text = content

        doc = nlp(text)

        for entity in doc.ents:
            print(entity.text, entity.label_ )

        #tokens = nltk.word_tokenize(text)

        #tagged = nltk.pos_tag(tokens)

        #entities = nltk.chunk.ne_chunk(tagged)

        #print(entities)

