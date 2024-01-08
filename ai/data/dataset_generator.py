import os
import re
import random

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
        self.cities = list(df.keys())

        np.random.shuffle(self.cities)
        self.departures = self.cities[:int(len(self.cities) / 2)]
        self.arrivals = self.cities[int(len(self.cities) / 2):]

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

    @staticmethod
    def create_object_text_label(sentence: str, departure: str, arrival: str, prefix: str, name: str, correct: int, not_french: int, not_trip: int, unknown: int) -> dict:

        # Case for unclassified sentences with two times the same city
        if "{dup_departure}" in sentence:
            sentence = sentence.replace("{dup_departure}", "{arrival}")
            arrival = departure
        elif "{dup_arrival}" in sentence:
            sentence = sentence.replace("{dup_arrival}", "{departure}")
            departure = arrival

        # If no arrival, departure will always take prefix
        if not arrival:
            option = 0
        # If no departure, arrival will always take prefix
        elif not departure:
            option = 1
        # Else, randomize who takes prefix, one or both
        else:
            option = np.random.randint(0, 3)

        departure_prefix = f"{prefix}{departure}"
        arrival_prefix = f"{prefix}{arrival}"

        f_dict = {
            "departure": departure_prefix if option != 1 else departure,
            "arrival": arrival_prefix if option != 0 else arrival,
            "name": name
        }

        return {
            "text": sentence.format(**f_dict),
            "CORRECT": correct,
            "NOT_FRENCH": not_french,
            "NOT_TRIP": not_trip,
            "UNKNOWN": unknown
        }

    def fill_text_classification_sentences_templates(self, departure: str, arrival: str) -> list:

        correct_sentences = []
        wrong_sentences = []
        unclassified_sentences = []

        prefixes = [random.choice(self.prefixes)] + [("", "")]

        for prefix in prefixes:

            correct_sentences.extend([
                self.create_object_text_label(
                    sentence, departure, arrival, prefix[0], "",
                    1, 0, 0, 0
                )
                for sentence in self.correct_sentences
            ])

            correct_sentences.extend([
                self.create_object_text_label(
                    sentence, departure, arrival, prefix[0], np.random.choice(self.names),
                    1, 0, 0, 0
                )
                for sentence in self.correct_sentences_with_names
            ])

            unclassified_sentences.extend([
                self.create_object_text_label(
                    sentence, departure, arrival, prefix[0], "",
                    0, 0, 1, 0
                )
                for sentence in self.unclassified_sentences
            ])

            wrong_sentences.extend([
                self.create_object_text_label(
                    sentence, departure, "", prefix[0], "",
                    0, 0, 1, 0
                )
                for sentence in self.wrong_sentences["only_departure_fr"]
            ])

            wrong_sentences.extend([
                self.create_object_text_label(
                    sentence, "", arrival, prefix[0], "",
                    0, 0, 1, 0
                )
                for sentence in self.wrong_sentences["only_arrival_fr"]
            ])

            wrong_sentences.extend([
                self.create_object_text_label(
                    sentence, departure, arrival, prefix[1], "",
                    0, 1, 0, 0
                )
                for sentence in self.wrong_sentences["english"]
            ])

            wrong_sentences.extend([
                self.create_object_text_label(
                    sentence, departure, "", prefix[1], "",
                    0, 1, 1, 0
                )
                for sentence in self.wrong_sentences["only_departure_en"]
            ])

            wrong_sentences.extend([
                self.create_object_text_label(
                    sentence, "", arrival, prefix[1], "",
                    0, 1, 1, 0
                )
                for sentence in self.wrong_sentences["only_arrival_en"]
            ])

        sentences = []
        sentences.extend(unclassified_sentences)
        sentences.extend(wrong_sentences)

        np.random.shuffle(correct_sentences)
        sentences.extend(correct_sentences[:int(len(sentences))])
        return sentences

    @staticmethod
    def generate_text_classification_unknown_sentences(number: int) -> list:
        length = np.random.randint(16, 128)

        sentences = []

        for _ in range(int(number / 2)):
            sentences.append("".join([chr(np.random.randint(32, 127)) for _ in range(length)]))
            sentences.append("".join(np.random.choice(list("abcdefghijklmnopqrstuvwxyz      "), length)))

        for i, sentence in enumerate(sentences):
            sentences[i] = {
                "text": sentence,
                "CORRECT": 0,
                "NOT_FRENCH": 0,
                "NOT_TRIP": 0,
                "UNKNOWN": 1
            }

        return sentences

    def get_text_classification_batch_sentences(self, departure: str, arrival: str) -> list:
        data = []

        for case in self.cases:
            for special_char in [""] + self.special_chars:
                m_departure = getattr(departure, case)()
                m_arrival = getattr(arrival, case)()

                if special_char and special_char in m_departure:
                    m_departure = m_departure.replace(special_char, " ")
                if special_char and special_char in m_arrival:
                    m_arrival = m_arrival.replace(special_char, " ")

                data.extend(self.fill_text_classification_sentences_templates(m_departure, m_arrival))

        return data

    def flatten_list(self, nested_list):
        flattened_list = []
        for i in nested_list:
            if isinstance(i, list):
                flattened_list.extend(self.flatten_list(i))
            else:
                flattened_list.append(i)
        return flattened_list

    @staticmethod
    def split_sentence_token_classification(sentence: str) -> list:
        regex = r'[\w|?]+\S?'
        formatted_sentence = [s for s in re.findall(regex, sentence) if s]
        return formatted_sentence

    @staticmethod
    def manage_trailing_punctuation(sentence: list) -> tuple[list, bool]:
        if sentence[-1][-1] in [".", "?", "!"]:
            sentence[-1] = sentence[-1][:-1]
            sentence.append(".")
            return sentence, True
        return sentence, False

    @classmethod
    def format_sentence_token_classification(cls, sentence: str) -> tuple[list, bool]:
        formatted_sentence = cls.split_sentence_token_classification(sentence)
        sentence, should_add_dot = cls.manage_trailing_punctuation(formatted_sentence)
        return sentence, should_add_dot

    def prepare_sentences_token_classification(self) -> list:
        final_sentences = []

        for sentence in self.correct_sentences + self.correct_sentences_with_names:
            final_sentences.append(sentence.format(departure="{departure}", arrival="{arrival}", name="{name}"))

            random_fr_prefix = np.random.choice(self.fr_prefixes)

            final_sentences.append(np.random.choice([
                sentence.format(departure=random_fr_prefix + "{departure}", arrival="{arrival}", name="{name}"),
                sentence.format(departure="{departure}", arrival=random_fr_prefix + "{arrival}", name="{name}"),
                sentence.format(departure=random_fr_prefix + "{departure}", arrival=random_fr_prefix + "{arrival}", name="{name}")
            ]))

        return final_sentences

    def generate_ner_tags_from_correct_sentences(self, steps: dict, sentences: list) -> list:
        data = []

        for sentence in sentences:

            alt_sentence = sentence.replace("{", "").replace("}", "")
            formatted_sentence = self.split_sentence_token_classification(alt_sentence)

            tags_sentence = [self.ner_labels.index("O")] * (len(formatted_sentence))

            random_name = np.random.choice(self.names)

            for i, word in enumerate(formatted_sentence):
                if "departure" in word:
                    formatted_step = self.split_sentence_token_classification(steps["departure"])
                    tags_sentence[i] = [self.ner_labels.index("B-DEP")] + [self.ner_labels.index("I-DEP")] * (len(formatted_step) - 1)

                if "arrival" in word:
                    formatted_step = self.split_sentence_token_classification(steps["arrival"])
                    tags_sentence[i] = [self.ner_labels.index("B-ARR")] + [self.ner_labels.index("I-ARR")] * (len(formatted_step) - 1)

                if "name" in word:
                    formatted_name = self.split_sentence_token_classification(random_name)
                    tags_sentence[i] = [self.ner_labels.index("O")] * len(formatted_name)

            # remove 2D list inside list
            tags_sentence = self.flatten_list(tags_sentence)

            final_sentence = sentence.format(departure=steps["departure"], arrival=steps["arrival"], name=random_name)

            formatted_final_sentence, should_add_dot = self.format_sentence_token_classification(final_sentence)
            if should_add_dot:
                tags_sentence.append(self.ner_labels.index("O"))

            data.append({
                "text": final_sentence,
                "tokens": formatted_final_sentence,
                "ner_tags": tags_sentence,
            })

        return data

    def generate_ner_tags_from_random_sentences(self, random_sentences: list) -> list:
        for random_sentence in random_sentences:
            sentence = random_sentence["text"]
            formatted_sentence, _ = self.format_sentence_token_classification(sentence)
            tags_sentence = [self.ner_labels.index("O")] * (len(formatted_sentence))
            random_sentence["tokens"] = formatted_sentence
            random_sentence["ner_tags"] = tags_sentence
        return random_sentences

    def generate_text_classification_dataset(self, regenerate=False):
        path = "text_classification/"

        print("Generating text classification dataset...")
        if os.path.exists(path) and not regenerate:
            print("Folder already exists, skipping generation.")
            return
        else:
            os.makedirs(path, exist_ok=True)
            for file in os.listdir(path):
                os.remove(os.path.join(path, file))

        dataset = []
        arrivals = self.arrivals.copy()

        for departure in self.departures:
            # pick random arrival and remove it from list
            arrival = np.random.choice(arrivals)
            arrivals.remove(arrival)
            dataset.extend(self.get_text_classification_batch_sentences(departure, arrival))

        # Create dataframe
        df = pd.DataFrame(dataset)

        # Delete duplicates on text column
        df = df.drop_duplicates(subset=["text"])

        # get number of rows where CORRECT is 1
        length = len(df[df["CORRECT"] == 1])

        # Add random sentences to dataset
        np.random.shuffle(self.random_sentences)
        random_sentences = self.random_sentences[:int(length / 2)]

        # Add unknown sentences in the dataset
        unknown_sentences = self.generate_text_classification_unknown_sentences(length)
        df = pd.concat([df, pd.DataFrame(random_sentences), pd.DataFrame(unknown_sentences)])

        # Delete duplicates again on text column
        df = df.drop_duplicates(subset=["text"])

        # Shuffle dataset since random sentences at the end weight more in file size
        df = df.sample(frac=1).reset_index(drop=True)

        number_files = 4
        for id, df_i in enumerate(np.array_split(df, number_files)):
            df_i.to_csv(f"{path}dataset_text_classification_{id + 1}.csv", index=False, sep=";")

        print(f"Dataset generated with {len(df)} sentences.")

    def generate_token_classification_dataset(self, regenerate=False):
        path = "token_classification/"

        print("Generating token classification dataset...")
        if os.path.exists(path) and not regenerate:
            print("Folder already exists, skipping generation.")
            return
        else:
            os.makedirs(path, exist_ok=True)
            for file in os.listdir(path):
                os.remove(os.path.join(path, file))

        dataset = []

        # prepare templates from correct sentences to generate strings for token classification
        sentences = self.prepare_sentences_token_classification()

        arrivals = self.arrivals.copy()

        for departure in self.departures:
            arrival = np.random.choice(arrivals)
            arrivals.remove(arrival)
            steps = {"departure": departure, "arrival": arrival}

            for special_char in [""] + self.special_chars:
                for k, step in steps.items():
                    steps[k] = getattr(step, np.random.choice(self.cases))()

                    if special_char and special_char in step:
                        steps[k] = step.replace(special_char, " ")

                    dataset.extend(self.generate_ner_tags_from_correct_sentences(steps, sentences))

        # Add random sentences to dataset
        random_sentences = self.generate_ner_tags_from_random_sentences(self.random_sentences_french)
        dataset.extend(random_sentences)

        df = pd.DataFrame(dataset)

        # Drop duplicates on text column
        df = df.drop_duplicates(subset=["text"])

        # Shuffle dataset since random sentences at the end weight more in file size
        df = df.sample(frac=1).reset_index(drop=True)

        number_files = 4
        for id, df_i in enumerate(np.array_split(df, number_files)):
            df_i.to_csv(f"{path}dataset_token_classification_{id + 1}.csv", index=False, sep=";")

        print(f"Dataset generated with {len(df)} sentences.")


if __name__ == "__main__":
    generator = DatasetGenerator()
    generator.generate_text_classification_dataset(True)
    generator.generate_token_classification_dataset(True)
