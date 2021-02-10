import io
from model import pairwise

LAMBDA1 = 0.66
LAMBDA2 = 0.33
LAMBDA3 = 0.01
EPSILON = 0.00001

def build_test_set(address):
    f = io.open(address, mode="rt", encoding="utf-8")
    data = f.read()
    verses = data.split('\n')[0:-1]
    classified = [verse.split('\t') for verse in verses]
    classes = [int(classified[i][0]) for i in range(len(classified))]
    verses = [classified[i][1] for i in range(len(classified))]
    return classes, verses

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

def evaluate_models(results, tests, models):
    result = determine_poet(tests, models)
    
    true_count = 0
    for i in range(len(results)):
        if results[i] == result[i]:
            true_count += 1
    return true_count / len(results)


def evaluate(address, uni_models, bi_models):
    results, tests = build_test_set(address)
    uni_accuracy = evaluate_models(results, tests, uni_models)
    bi_accuracy = evaluate_models(results, tests, bi_models)
    return uni_accuracy, bi_accuracy