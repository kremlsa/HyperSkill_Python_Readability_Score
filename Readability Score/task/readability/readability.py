# write your code here
import argparse
import math
import re


class Evaluator:
    vowels = ["a", "e", "i", "o", "u", "y"]
    ratings = {1: ["about 6-year-olds", 6],
               2: ["about 7-year-olds", 7],
               3: ["about 9-year-olds", 9],
               4: ["about 10-year-olds", 10],
               5: ["about 11-year-olds", 11],
               6: ["about 12-year-olds", 12],
               7: ["about 13-year-olds", 13],
               8: ["about 14-year-olds", 14],
               9: ["about 15-year-olds", 15],
               10: ["about 16-year-olds", 16],
               11: ["about 17-year-olds", 17],
               12: ["about 18-year-olds", 18],
               13: ["about 24-year-olds", 24],
               14: ["about 25-year-olds", 25]}

    def __init__(self, text_, dict_):
        self.text = text_.strip()
        self.common_words = self.load_words(dict_)

    def load_words(self, dict_):
        with open(dict_) as file_:
            text_ = file_.read()
        return text_.split()

    @property
    def word_count(self):
        return len(self.text.split())

    @property
    def difficult(self):
        count_ = 0
        for word_ in self.text.split():
            word_ = word_.lower()
            word_ = re.sub(r"[(),.!?]", '', word_)
            if word_ not in self.common_words:
                count_ += 1
        return count_

    @property
    def diff_score(self):
        score_ = 0.1579 * 100 * self.difficult / self.word_count + 0.0496 * self.word_count / self.sentence_count
        if self.difficult * 100 / self.word_count >= 5.0:
            score_ += 3.6365
        return round(score_, 2)

    @property
    def sentence_count(self):
        return len(re.split(r"[.?!]\s", self.text))

    @property
    def chars_count(self):
        return len(re.sub(r"[\s]", "", self.text))

    @property
    def score(self):
        return round(4.71 * self.chars_count / self.word_count + 0.5 * self.word_count / self.sentence_count - 21.43, 2)

    def rating(self, value_):
        return self.ratings[round(value_)][0]

    def diff_rating(self, value_):
        if value_ <= 4.9:
            return 10
        elif value_ <= 5.9:
            return 12
        elif value_ <= 6.9:
            return 14
        elif value_ <= 7.9:
            return 16
        elif value_ <= 9.9:
            return 18
        elif value_ <= 9.9:
            return 24
        else:
            return 25

    @property
    def syl_count(self):
        count_=0
        for word_ in self.text.split():
            word_ = word_.lower()
            count_ += self.count_syl(word_)
        return count_

    @property
    def poly_count(self):
        count_=0
        for word_ in self.text.split():
            finds_ = self.count_syl(word_)
            if finds_ > 2:
                count_ += 1
        return count_

    def count_syl(self, word_):
        count_ = 0
        is_vowel = False
        count_e_ = 0
        word_vowels_ = 0
        for char_ in word_:
            if char_ in self.vowels:
                word_vowels_ += 1
                if not is_vowel:
                    count_ += 1
                    is_vowel = True
            else:
                is_vowel = False
        if re.match(r".+[bcdfghjklmnpqrstvwxyz]+e[.?!]*$", word_) and word_vowels_ > 1:
            count_e_ += 1
        if word_vowels_ == 0:
            count_ += 1
        return count_ - count_e_

    @property
    def f_k_score(self):
        return round(0.39 * self.word_count / self.sentence_count + 11.8 * self.syl_count / self.word_count - 15.59, 2)

    @property
    def smog_score(self):
        return round(1.043 * pow(self.poly_count * 30 / self.sentence_count, 0.5) + 3.1291, 2)

    @property
    def c_l_score(self):
        s_ = self.sentence_count / self.word_count * 100.0
        l_ = self.chars_count / self.word_count * 100.0
        return round(0.0588 * l_ - 0.296 * s_ - 15.8, 2)

    def ari(self):
        print("Automated Readability Index: {} ({})".format(self.score, self.rating(math.floor(self.score))))

    def f_k(self):
        print("Flesch–Kincaid readability tests: {} ({})".format(self.f_k_score, self.rating(self.f_k_score)))

    def smog(self):
        print("Simple Measure of Gobbledygook: {} ({})".format(self.smog_score, self.rating(self.smog_score)))

    def c_l(self):
        print("Coleman–Liau index: {} ({})".format(self.c_l_score, self.rating(self.c_l_score)))

    def pb(self):
        print("Probability-based score: {} (about {}-year-olds)".format(self.diff_score, self.diff_rating(self.diff_score)))

    @property
    def mean(self):
        return round((self.ratings[math.floor(self.score)][1] + self.ratings[round(self.smog_score)][1]
                      + self.ratings[round(self.f_k_score)][1] + self.ratings[round(self.c_l_score)][1]
                      + self.diff_rating(self.diff_score)) / 5, 2)


parser = argparse.ArgumentParser(description="This programm counts readability score.")
parser.add_argument("--infile")
parser.add_argument("--words")
args = parser.parse_args()
filename = args.infile
with open(filename) as file:
    text = file.read()
evaluator = Evaluator(text, args.words)
print("The text is:")
print(evaluator.text)
print("Words: {}".format(evaluator.word_count))
print("Difficult words: {}".format(evaluator.difficult))
print("Sentences: {}".format(evaluator.sentence_count))
print("Characters: {}".format(evaluator.chars_count))
print("Syllables: {}".format(evaluator.syl_count))
print("Polysyllables: {}".format(evaluator.poly_count))
print("Enter the score you want to calculate (ARI, FK, SMOG, CL, PB, all):", end="")
choice = input()
print()
if choice == "ARI":
    evaluator.ari()
if choice == "FK":
    evaluator.f_k()
if choice == "SMOG":
    evaluator.smog()
if choice == "CL":
    evaluator.c_l()
if choice == "PB":
    evaluator.pb()
if choice == "all":
    evaluator.ari()
    evaluator.f_k()
    evaluator.smog()
    evaluator.c_l()
    evaluator.pb()
print()
print("This text should be understood in average by {}-year-olds.".format(evaluator.mean))
