from model import get_models
from test import evaluate

files = ["ferdowsi_train.txt", "hafez_train.txt", "molavi_train.txt"]
models = get_models(files)
print(evaluate("test_set/test_file.txt", models))