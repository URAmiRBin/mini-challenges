import io

def build_test_set(address):
    f = io.open(address, mode="rt", encoding="utf-8")
    data = f.read()
    verses = data.split('\n')[0:-1]
    classified = [verse.split('\t') for verse in verses]
    classes = [int(classified[i][0]) for i in range(len(classified))]
    verses = [classified[i][1] for i in range(len(classified))]
    return classes, verses

def compute_ps(test, models):
    ps = []
    for model in models:
        ps.append(1)
        for word in test:
            try:
                ps[-1] *= model[word]
            except:
                ps[-1] *= 0.001
    return ps

def determine_poet(tests, models):
    result = []
    for test in tests:
        ps = compute_ps(test, models)
        result.append(ps.index(max(ps)) + 1)
    return result

def evaluate(address, models):
    results, tests = build_test_set(address)
    result = determine_poet(tests, models)
    print(result[2500:2550])
    print(results[2500:2550])

    true_count = 0
    for i in range(len(results)):
        if results[i] == result[i]:
            true_count += 1
    return true_count / len(results)