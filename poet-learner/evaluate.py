import io
from model import pairwise

# Settings
LAMBDA1 = 0.66
LAMBDA2 = 0.33
LAMBDA3 = 0.01
EPSILON = 0.00001

# Get an address for test cases and convert tests into two lists
# ith item in classes denotes poet index of corresponding poem in verses list
def build_test_set(address):
    f = io.open(address, mode="rt", encoding="utf-8")
    data = f.read()
    verses = data.split('\n')[0:-1]
    classified = [verse.split('\t') for verse in verses]
    classes = [int(classified[i][0]) for i in range(len(classified))]
    verses = [classified[i][1] for i in range(len(classified))]
    return classes, verses

# Get a test and a list of unigram models and compute probability of that test happening in each model
# return a list of proabilities corresponding to each model
# If a word was in test and was not in the model, use EPSILON to smooth the probability
def compute_uni_ps(test, models):
    ps = []
    for model in models:
        ps.append(1)
        for word in test:
            try:
                ps[-1] *= model[word]
            except:
                ps[-1] *= EPSILON
    return ps

# Get a test and a list of bigram models and compute probability of that test happening in each model
# return a list of proabilities corresponding to each model
# Use backoff model to smooth the probability
def compute_bi_ps(test, models):
    ps = []
    for model in models:
        ps.append(1)
        for pair in test:
            try:
                ps[-1] *= LAMBDA1 * model[pair] + LAMBDA2 * model[pair[1]] + LAMBDA3 * EPSILON
            except:
                try:
                    ps[-1] *= LAMBDA2 * model[pair[1]] + LAMBDA3 * EPSILON
                except:
                    ps[-1] *= LAMBDA3 * EPSILON
    return ps

# Get a list of tests and a list of models and return a list of guesses for each test
# The ith element of result corresponds to the ith element of tests
# PROTOCOL: If first element of model is a pair, then it's a bigram pair
def determine_poet(tests, models):
    tests = [test.split(" ") for test in tests]
    isBi = type(list(models[0].keys())[0]) is tuple
    if isBi:
        start_symbol = "<s>"
        tests = [[start_symbol] + test for test in tests]
        tests = pairwise(tests)
    result = []
    for test in tests:
        if isBi:
            ps = compute_bi_ps(test, models)
        else:
            ps = compute_uni_ps(test, models)
        result.append(ps.index(max(ps)) + 1)
    return result

# Count correct guesses to calculate the accuracy
def evaluate_models(results, tests, models):
    result = determine_poet(tests, models)
    
    true_count = 0
    for i in range(len(results)):
        if results[i] == result[i]:
            true_count += 1
    return true_count / len(results)

# Get address of test file and an unigram and a bigram model
# Return models accuracy respectively
def evaluate(address, uni_models, bi_models):
    results, tests = build_test_set(address)
    uni_accuracy = evaluate_models(results, tests, uni_models)
    bi_accuracy = evaluate_models(results, tests, bi_models)
    return uni_accuracy, bi_accuracy