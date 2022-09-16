import pandas as pd
import nltk
from nltk.corpus import words
nltk.download('words')
nltk.download('punkt')
data = pd.read_csv("./words.txt", sep=",")
array = data["Words"]
# f = open("words.txt", "r")
# words = f.read()
# print(words)
# print(array)
data.drop('0', inplace=True)
print(data)
# for i in range(array.size):
#     if array[i] in words.words():
#         array.drop(array[i], inplace=True)
#         print(array[i])

    # print(array[i])
# tokens = nltk.word_tokenize(words)
# print(tokens)