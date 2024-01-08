"""
Original dataset comes from: https://www.kaggle.com/datasets/chazzer/big-language-detection-dataset/data
"""

import os
import pandas as pd
import numpy as np


def main():
    dir_path = os.path.join(os.path.abspath(__file__), "..", "sentences")
    path = os.path.join(dir_path, "sentences.csv")
    df = pd.read_csv(path, sep=",")

    # keep only certain languages
    df = df[df["lan_code"].isin(["fra", "eng", "spa", "ita", "deu"])]

    # rename columns
    df = df.rename(columns={"lan_code": "Language", "sentence": "Text"})

    # shuffle the dataset
    df = df.sample(frac=1).reset_index(drop=True)

    # take a third of the dataset
    df = df.iloc[:int(len(df) / 2)]

    number_files = 3
    for id, df_i in enumerate(np.array_split(df, number_files)):
        df_i.to_csv(f"{dir_path}/random_sentences_{id + 1}.csv", index=False, sep=";")


if __name__ == '__main__':
    main()
