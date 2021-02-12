# mini-challenges
:brain: Some coding challenges that need critical thinking

## [Colored Sudoku](https://github.com/URAmiRBin/mini-challenges/tree/main/sudoku)

In this challenge given a sudoku table and a list of colors, which their order represents their priority, a mix of Sudoku and Color-mapping problem is solved.

Rules:
  - No repeated numbers in rows
  - No repeated numbers in columns
  - No neighbors should have the same colors
  - If a neighbor has a smaller number, its' color must have less priority
  
> NOTE: table size must be at most 9 and colors must be represented with one character

Input example:
```
5 3
r g b y p
1# *b *#
*# 3r *#
*g 1# *#
```

This means we have 5 colors and a 3 x 3 table. Empty colors and numbers are represented with # and * respectively.

This challenge is solved using **minimum remaining value** heuristic and is sped up using **forward-checking**.

[Farsi specification file](https://github.com/URAmiRBin/mini-challenges/blob/main/sudoku/spec.pdf)

## [Poet learner](https://github.com/URAmiRBin/mini-challenges/tree/main/poet-learner)

In this challenge, using simple probabilistic methods, treating each poet's vocabulary of use, a unigram and bigram model is build to guess poet of new verses.

Steps:
  - Read training files
  - Build unigram and bigram models for each poet
  - Read test files
  - Evaluate
  
I achieved 80% accuracy for unigram and 84% for bigram models.

To test with custom verses use `python guess.py` and type in your verse.

> NOTE: Use a command line tool that supports utf-8 and farsi characters.

I used **backoff model** for smoothing. the parameters lambda and epsilon can be tuned in test.py

[Farsi specification file](https://github.com/URAmiRBin/mini-challenges/blob/main/poet-learner/spec.pdf)
