import io
from collections import Counter
import itertools

def build_uni_dic(address):
    f = io.open(address, mode="rt", encoding="utf-8")
    data = f.read()
    words = data.split()
    words_counter = Counter(words)
    return words_counter

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

def pairwise(iterables):
    result = []
    for iterable in iterables:
        a, b = itertools.tee(iterable)
        next(b, None)
        result.append(list(zip(a, b)))
    return result


def prune_dic(dictionary, thresh):
    return {k: v for k, v in dict.items(dictionary) if v > thresh}

def build_unigram_model(dictionary):
    size = len(dictionary)
    model = dictionary
    for word in dictionary:
        model[word] = dictionary[word] / size
    return model

def get_uni_models(files):
    models = []
    for i in range(len(files)):
        models.append({})
        dictionary = build_uni_dic("train_set/" + files[i])
        pruned_dictionary = prune_dic(dictionary, 2)
        models[i] = build_unigram_model(pruned_dictionary)
    return models

def build_bi_model(p_dictionary, s_dictionary):
    s_size = len(s_dictionary)
    model = {}
    for pair in p_dictionary:
        model[pair] = p_dictionary[pair] / s_dictionary[pair[0]]
    for word in s_dictionary:
        model[word] = s_dictionary[word] / s_size
    return model
        
def get_bi_models(files):
    models = []
    for i in range(len(files)):
        models.append({})
        pair_dictionary, verse_count = build_bi_dic("train_set/" + files[i])
        pair_dictionary = prune_dic(pair_dictionary, 2)
        single_dictionary = prune_dic(build_uni_dic("train_set/" + files[i]), 2)
        single_dictionary["<s>"] = verse_count
        models[i] = build_bi_model(pair_dictionary, single_dictionary)
    return models
