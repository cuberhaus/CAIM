import pandas as pd
import datetime
import matplotlib
from tqdm import tqdm

print("hola.com".isalpha())
path_words = "./words.txt"
df = pd.read_csv(path_words, sep=", ", header=0)

c_deleted = 0

# lio de indices, no recomendable
# for i in range(len(df)):
#    word = df.iloc[i, 1]
#    if not word.isalpha():
#        #print("Antes:" + str(i))
#        df.drop(index=i, inplace=True)
# c_deleted += 1
# print("Depsues:" + str(i))
# print(i)
# print(word)
# if i-1 >= 0:
# print(df.iloc[i-1, 0], df.iloc[i-1, 1])
# df.drop([0,1,2], inplace=True)

for index, row in tqdm(df.iterrows(), "Rows:"):
    word = str(row[1])  # Must convert to string cause there are some floats
    if not word.isalpha():
        # print("Antes:" + str(i))
        df.drop(index=index, inplace=True)

print(df)
df.to_csv("./data" + str(datetime.datetime.now()) + ".csv", index=False, header=True, sep='\t')





