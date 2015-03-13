from collections import Counter, OrderedDict 
import json
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from pprint import pprint

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
        mdr_text[event_key] = '. '.join(mdr_text[event_key])

        # Tokenize & Tag with nltk
        #text = nltk.word_tokenize(mdr_text[event_key])
        text = tokenizer.tokenize(mdr_text[event_key])

        # Don't remove stopwords & numbers yet, as doing so may affect the part of speech (?)
        counter = Counter(nltk.pos_tag(text))
        parsed[event_key] = {}

        # Ignore stopwords, punctuation, and numbers
        for word_pair, frequency in counter.most_common():
          word, part_of_speech = word_pair
          if word.lower() in stopwords.words('english') or word.isdigit() or len(word) <= 1:
            continue

  #        if frequency < frequency_threshold:
  #          continue

          new_entry = OrderedDict()
          new_entry["part_of_speech"] = part_of_speech
          new_entry["count"] = frequency

          parsed[event_key][word] = new_entry
  return parsed

def write_json_to_file(j, output_filename):
  with open(output_filename, "w") as output_file:
    json.dump(j, output_file, indent=4)  

def read_json_from_file(input_filename):
  input_json = None
  with open(input_filename, "r") as f:
    input_json = json.loads(f.read())
  return input_json

#   weka_file = open("weka.arff", "w")

def generate_weka_data(parsed, weka_filename):
  # Get a set of all words used
  all_words = set()
  for event_key, words in parsed.items():
    all_words.update(words.keys())
  all_words = list(all_words)

  weka_file = open(weka_filename, "w")
  weka_file.write("@relation seng474\n")
  for word in all_words:
    weka_file.write("@attribute {} NUMERIC\n".format(word))
  weka_file.write("@data\n")

  for event_key, words in parsed.items():
    count_string = [0] * len(all_words)

    for word, count in words.items():
      index = all_words.index(word)
      count_string[index] = count["count"]

    weka_file.write(','.join([str(x) for x in count_string]))
    weka_file.write('\n')

  weka_file.close()


def main():
  # parsed = parse_maude_data(filename="output.txt")
  # write_json_to_file(parsed, output_filename="word_frequencies.txt")
  parsed = read_json_from_file("word_frequencies.txt")
  generate_weka_data(parsed, weka_filename="weka.arff")

if __name__ == '__main__':
  main()