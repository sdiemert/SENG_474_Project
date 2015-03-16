from collections import Counter, OrderedDict 
import itertools
import json
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from pprint import pprint
import os
import random

def parse_maude_data(filename):
  """
  Given a filename in the same directory of the script, parse the 
  JSON of medical event records from MAUDE to return the following dictionary:

  dictionary[event_key][word] = {
    "count": Count of the word appearing in "mdr_text" of the JSON entry
    "part_of_speech": Part of speech as defined by the nltk with the taggers/maxent_treebank_pos_tagger/english.pickle file.
  }
  """

  parsed = OrderedDict()
  # If the count of word is less than FREQUENCY_THRESHOLD, ignore
  frequency_threshold = 2
  tokenizer = RegexpTokenizer(r'[a-zA-Z0-9_-]+')

  with open(filename, "r") as f:
    mdr_text = {} 
    parsed = OrderedDict()

    data = json.loads(f.read())

    for entry in data:
      event_key = entry["event_key"]

      if "mdr_text" in entry and entry["mdr_text"]:
        mdr_text[event_key] = []
        # Join all entries in the mdr_text list
        for mdr_text_entry in entry["mdr_text"]:
          if "text" in mdr_text_entry:
            mdr_text[event_key].append(mdr_text_entry["text"])
        mdr_text[event_key] = '. '.join(mdr_text[event_key]).lower()

        # Tokenize & Tag with nltk
        #text = nltk.word_tokenize(mdr_text[event_key])
        text = tokenizer.tokenize(mdr_text[event_key])

        # Don't remove stopwords & numbers yet, as doing so may affect the part of speech (?)
        counter = Counter(nltk.pos_tag(text))
        parsed[event_key] = {}

        # Ignore stopwords, punctuation, and numbers
        for word_pair, frequency in counter.most_common():
          word, part_of_speech = word_pair
          if word.lower() in stopwords.words('english') or word.isdigit() or len(word) <= 4:
            continue

  #        if frequency < frequency_threshold:
  #          continue

          new_entry = OrderedDict()
          new_entry["part_of_speech"] = part_of_speech
          new_entry["count"] = frequency

          parsed[event_key][word] = new_entry
  return parsed

# http://stackoverflow.com/a/16915734
def powerset(iterable):
  xs = list(iterable)
  return itertools.chain.from_iterable(itertools.combinations(xs, n) for n in range(1, len(xs) + 1))

def generate_weka_data(parsed):
  """
  For each class value, we build a WEKA file for only that class.
  Given our classes = {PointOfDecision, PointOfCare, CareProvider, MDDS, EMR, TechnicalProcess, HealthCareProcess},
  the first classifier will take the given tuple and answer "Is this tuple in the PointOfDecision class or not?",
  and the second classfier will answer "Is this tuple in the PointOfCare class or not?" and so on.
  """

  # Read classes such as PointOfDecision or PointOfCare
  classes = read_json_from_file("categorized_records.json")
  class_values = classes[random.choice(classes.keys())].keys()
  # Get a set of all words used
  all_words = set()
  for event_key, words in parsed.items():
    for word, word_metadata in words.items():
      if word_metadata["part_of_speech"].startswith("NN"):
        all_words.add(word)
  all_words = list(all_words)
  
  word_count_strings = {}

  # Update word frequencies in the @data string for WEKA
  for event_key, words in parsed.items():
    if event_key not in classes:
      continue

    word_count_strings[event_key] = [0] * len(all_words)

    for word, word_metadata in words.items():
      if not word_metadata["part_of_speech"].startswith("NN"):
        # print "Ignoring {}: {}".format(word, word_metadata["part_of_speech"])
        continue
      index = all_words.index(word)
      word_count_strings[event_key][index] = word_metadata["count"]

  for current_class in class_values:
    # Write metadata for the ARFF file
    weka_file = open("{}/weka/{}.arff".format(os.getcwd(), current_class), "w")
    weka_file.write("@relation seng474\n")
    for word in all_words:
      weka_file.write("@attribute {} NUMERIC\n".format(word))
    weka_file.write("@attribute {} {{0, 1}}\n".format(current_class))
    weka_file.write("@data\n")

    for event_key, words in parsed.items():
      if event_key not in classes:
        continue

      weka_file.write(','.join([str(x) for x in word_count_strings[event_key]]))
      weka_file.write(',' + ["0", "1"][classes[event_key][current_class] > 0])
      weka_file.write('\n')
    weka_file.close()

def write_json_to_file(j, output_filename):
  with open(output_filename, "w") as output_file:
    json.dump(j, output_file, indent=4)  


def read_json_from_file(input_filename):
  input_json = None
  with open(input_filename, "r") as f:
    input_json = json.loads(f.read())
  return input_json


def main():
  # parsed = parse_maude_data(filename="output.txt")
  print ("Finished parsing MAUDE data...")
  # write_json_to_file(parsed, output_filename="word_frequencies.txt")
  parsed = read_json_from_file("word_frequencies.txt")
  print ("Generating WEKA data...")

  generate_weka_data(parsed)
  print ("Finished.")

if __name__ == '__main__':
  main()