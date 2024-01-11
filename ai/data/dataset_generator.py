import os

import pandas as pd
import numpy as np


class DatasetGenerator:

    departures = []
    arrivals = []

    names = []

    correct_sentences = []
    correct_sentences_with_names = []

    wrong_sentences = {
        "english": [],
        "only_departure_fr": [],
        "only_arrival_fr": [],
        "only_departure_en": [],
        "only_arrival_en": [],
    }
    unclassified_sentences = []
    random_sentences = []
    random_sentences_french = []

    prefixes = [
        ("la ville de ", "the city of "),
        ("la place centrale de ", "the central square of "),
        ("la gare de ", "the train station of "),
        ("l'aéroport de ", "the airport of "),
        ("l'hopital de ", "the hospital of "),
    ]

    fr_prefixes = [prefix for prefix, _ in prefixes]

    cases = ["lower", "title", "upper"]
    special_chars = ["-", "/"]

    ner_labels = ["O", "B-DEP", "I-DEP", "B-ARR", "I-ARR"]

    def __init__(self):
        self.load_cities()
        print(len(self.departures), "departures loaded.")
        print(len(self.arrivals), "arrivals loaded.")

        if len(self.departures) != len(self.arrivals):
            raise Exception("Departures and arrivals are not the same length.")

        self.load_french_national_names()
        print(len(self.names), "names loaded.")

        self.correct_sentences = self.load_txt_sentences("correct_sentences")
        print(len(self.correct_sentences), "correct sentences loaded.")

        self.correct_sentences_with_names = self.load_txt_sentences("correct_sentences_with_names")
        print(len(self.correct_sentences_with_names), "correct sentences with names loaded.")

        self.unclassified_sentences = self.load_txt_sentences("unclassified_sentences")
        print(len(self.unclassified_sentences), "unclassified sentences loaded.")

        for key in self.wrong_sentences.keys():
            self.wrong_sentences[key] = self.load_txt_sentences(f"wrong_sentences_{key}")
            print(len(self.wrong_sentences[key]), f"wrong sentences {key} loaded.")

        self.load_random_sentences()
        print(len(self.random_sentences), "random sentences loaded.")

    @staticmethod
    def load_txt_sentences(filename: str) -> list:
        path = os.path.join(os.path.abspath(__file__), "..", "sentences", f"{filename}.txt")
        sentences = []
        with open(path, "r") as f:
            sentences = f.read().splitlines()
        return [sentence for sentence in sentences if sentence]

    def load_french_national_names(self):
        path = os.path.join(os.path.abspath(__file__), "..", "sentences", "french_national_names.csv")
        df = pd.read_csv(path, sep=",")
        self.names = list(df["name"].unique())

    def load_cities(self):
        path = os.path.join(os.path.abspath(__file__), "..", "..", "..", "backend", "path_finder", "data", "graph.json")
        df = pd.read_json(path)
        cities = list(df.keys())

        np.random.shuffle(cities)
        self.departures = cities[:int(len(cities) / 2)]
        self.arrivals = cities[int(len(cities) / 2):]

    def load_random_sentences(self):
        df_temp = []
        for file in os.listdir(os.path.join(os.path.abspath(__file__), "..", "sentences")):
            if file.endswith(".csv") and "random_sentences" in file:
                df_temp.append(pd.read_csv(os.path.join(os.path.abspath(__file__), "..", "sentences", file), sep=";"))

        df = pd.concat(df_temp, ignore_index=True)

        # keep a sixth of the dataset
        df = df.iloc[:int(len(df) / 6)]

        df["Language"] = df["Language"].apply(lambda x: 0 if x == "fra" else 1)

        # create a list of sentences, with column Text to key text, and NOT_FRENCH to key Language
        # also set NOT_TRIP to 1, UNKNOWN to 0 and CORRECT to 0
        self.random_sentences = ((df[["Text", "Language"]]
                                  .rename(columns={"Text": "text", "Language": "NOT_FRENCH"}))
                                 .assign(NOT_TRIP=1, UNKNOWN=0, CORRECT=0).to_dict(orient="records"))

        # keep only where Language is 0 (French)
        df = df[df["Language"] == 0]
        self.random_sentences_french = ((df[["Text"]].rename(columns={"Text": "text"})).to_dict(orient="records"))
