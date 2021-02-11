import io
from collections import Counter
import itertools

# Read the training file and return unigram dictionary
# return a dictionary with keys as words in file and values as respective occurrences
def build_uni_dic(address):
    f = io.open(address, mode="rt", encoding="utf-8")
    data = f.read()
    words = data.split()
    words_counter = Counter(words)
    return words_counter

# Read the training file and return bigram dictionary
# return a dictionary with keys as word pairs and values as respective occurrences
# <s> denotes start of a string and will be used in backoff model
def build_bi_dic(address):
    f = io.open(address, mode="rt", encoding="utf-8")
    data = f.read()
    verses = data.split("\n")
    verse_count = len(verses)
    verses = [verses[i].split(" ") for i in range(len(verses))]
    start_symbol = "<s>"
    verses = [[start_symbol] + verses[i] for i in range(len(verses))]
    pairs = pairwise(verses)
    flat_paris = [item for sublist in pairs for item in sublist]
    pairs_counter = Counter(flat_paris)
    return pairs_counter, verse_count

# Get a list of lists of words and return a lists of lists of pairs
# example: [['a', 'b', 'c']] => [[('a', 'b'), ('b', 'c')]]
def pairwise(iterables):
    result = []
    for iterable in iterables:
        a, b = itertools.tee(iterable)
        next(b, None)
        result.append(list(zip(a, b)))
    return result

# Get a dictionary of words and remove words with value less than threshold
def prune_dic(dictionary, thresh):
    return {k: v for k, v in dict.items(dictionary) if v > thresh}

# Get a dictionary and build a unigram model of it
# The model is also a dictionary with values set to probability of a word occurring 
def build_unigram_model(dictionary):
    size = sum(dictionary.values())
    model = dictionary
    for word in dictionary:
        model[word] = dictionary[word] / size
    return model

# Get two dictionaries, one for pairs and one for single words
# return a bigram model
# the model is a dictionary with keys set to pairs or single words
# and values set to their probability
def build_bi_model(p_dictionary, s_dictionary):
    size = sum(s_dictionary.values())
    model = {}
    for pair in p_dictionary:
        model[pair] = p_dictionary[pair] / s_dictionary[pair[0]]
    for word in s_dictionary:
        model[word] = s_dictionary[word] / size
    return model

# Get an array of train files and return respective unigram models
def get_uni_models(files):
    models = []
    for i in range(len(files)):
        models.append({})
        dictionary = build_uni_dic("train_set/" + files[i])
        pruned_dictionary = prune_dic(dictionary, 2)
        models[i] = build_unigram_model(pruned_dictionary)
    return models

# Get an array of train files and return respective bigram models
def get_bi_models(files):
    models = []
    for i in range(len(files)):
        models.append({})
        pair_dictionary, verse_count = build_bi_dic("train_set/" + files[i])
        pair_dictionary = prune_dic(pair_dictionary, 2)
        single_dictionary = build_uni_dic("train_set/" + files[i])
        single_dictionary = prune_dic(single_dictionary, 2)
        single_dictionary["<s>"] = verse_count
        models[i] = build_bi_model(pair_dictionary, single_dictionary)
    return models
