import argparse
import os

import pandas as pd
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser()

    # Read file
    parser.add_argument('--path', required=True, default=None, help='Path to the files')
    path_words = parser.parse_args().path
    df = pd.read_csv(path_words, sep=", ", header=0)

    # We erase the last two rows
    df = df.iloc[:-2]

    # Filter out non alpha "words"
    for index, row in tqdm(df.iterrows(), "Rows:"):
        word = str(row[1])  # Must convert to string cause there are some floats
        if not word.isalpha():
            df.drop(index=index, inplace=True)

    # Convert string to int
    df[df.columns[0]] = pd.to_numeric(df[df.columns[0]], errors='coerce')

    # Sort in descending order
    df.sort_values(by=df.columns[0], ascending=False, inplace=True)

    df.to_csv("./data_" + str(os.path.splitext(path_words)[0]) + ".csv", index=False, header=False, sep='\t')


if __name__ == '__main__':  # Executed when invoked directly, not when imported
    main()
