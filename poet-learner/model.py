import io
from collections import Counter

def build_dic(address):
    f = io.open(address, mode="rt", encoding="utf-8")
    data = f.read()
    words = data.split()
    words_counter = Counter(words)
    return words_counter

def prune_dic(dictionary, thresh):
    return {k: v for k, v in dict.items(dictionary) if v > thresh}

def build_unigram_model(dictionary):
    size = len(dictionary)
    model = dictionary
    for word in dictionary:
        model[word] = dictionary[word] / size
    return model

def get_models(files):
    models = []
    for i in range(len(files)):
        models.append({})
        dictionary = build_dic("train_set/" + files[i])
        pruned_dictionary = prune_dic(dictionary, 2)
        models[i] = build_unigram_model(pruned_dictionary)
    return models