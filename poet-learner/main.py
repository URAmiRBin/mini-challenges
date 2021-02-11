from model import get_uni_models, get_bi_models
from test import evaluate

# Build models
files = ["ferdowsi_train.txt", "hafez_train.txt", "molavi_train.txt"]
uni_models = get_uni_models(files)
bi_models = get_bi_models(files)

# Evaluate
uni_acc, bi_acc = evaluate("test_set/test_file.txt", uni_models, bi_models)
print("UNIGRAM ACCURACY : ", uni_acc )
print("BIGRAM  ACCURACY : ", bi_acc )
