from model import get_bi_models
from evaluate import determine_poet

# Build Bigram model which is slightly better than unigram
files = ["ferdowsi_train.txt", "hafez_train.txt", "molavi_train.txt"]
bi_models = get_bi_models(files)

poet_indices = {1: 'Ferdowsi', 2: 'Hafez', 3: 'Molavi'}

# Input and guess
# WARNING: You must use a command line tool that supports utf-8 for farsi
print("You tell your verse and I guess it's Ferdowsi, Hafez or Molavi")
user_verse = input("Enter you verse > ")
guess_index = determine_poet([user_verse], bi_models)[0]
print("Your verse is more like ", poet_indices[guess_index])