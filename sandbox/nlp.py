from collections import Counter, OrderedDict 
import json
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from pprint import pprint

# If the count of word is less than FREQUENCY_THRESHOLD, ignore
FREQUENCY_THRESHOLD = 2

with open("output.txt", "r") as f:
  data = json.loads(f.read())

  mdr_text = {} 
  word_frequencies = OrderedDict()
  tokenizer = RegexpTokenizer(r'\w+')

  for entry in data:
    event_key = entry["event_key"]

    if "mdr_text" in entry and entry["mdr_text"]:
      mdr_text[event_key] = []
      # Join all entries in the mdr_text list
      for mdr_text_entry in entry["mdr_text"]:
        if "text" in mdr_text_entry:
          mdr_text[event_key].append(mdr_text_entry["text"])
      mdr_text[event_key] = '. '.join(mdr_text[event_key])

      # Tokenize & Tag with nltk
      #text = nltk.word_tokenize(mdr_text[event_key])
      text = tokenizer.tokenize(mdr_text[event_key])

      # Don't remove stopwords & numbers yet, as doing so may affect the part of speech
      counter = Counter(nltk.pos_tag(text))
      word_frequencies[event_key] = {} 

      # Ignore stopwords, punctuation, and numbers
      for word_pair, frequency in counter.most_common():
        word, part_of_speech = word_pair
        if word.lower() in stopwords.words('english') or word.isdigit():
          continue
        
#        if frequency < FREQUENCY_THRESHOLD:
#          continue
        
        new_entry = OrderedDict()
        new_entry["part_of_speech"] = part_of_speech
        new_entry["count"] = frequency

        word_frequencies[event_key][word] = new_entry


with open("word_frequencies.txt", "w") as output_file:
  json.dump(word_frequencies, output_file, indent=4)

