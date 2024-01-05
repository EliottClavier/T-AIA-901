import os
import re

import pandas as pd
import numpy as np


class DatasetGenerator:

    cities = []
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

    ner_labels = ["O", "B-DEP", "I-DEP", "B-ARR", "I-ARR"]

    def __init__(self):
        self.load_cities()
        print(len(self.cities), "cities loaded.")

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
        self.random_sentences_french = ((df[["Text", "Language"]]
                                  .rename(columns={"Text": "text", "Language": "NOT_FRENCH"}))
                                 .assign(NOT_TRIP=1, UNKNOWN=0, CORRECT=0).to_dict(orient="records"))

    @staticmethod
    def create_object_text_label(sentence: str, departure: str, arrival: str, prefix: str, name: str, correct: int, not_french: int, not_trip: int, unknown: int) -> dict:
        f_dict = {
            "departure": np.random.choice((
                departure,
                f"{prefix}{departure}"
            )),
            "arrival": np.random.choice((
                arrival,
                f"{prefix}{arrival}"
            )),
            "name": name,
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

        for prefix in self.prefixes + [("", "")]:

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
                    sentence, departure, arrival, prefix[0], "",
                    0, 0, 1, 0
                )
                for sentence in self.wrong_sentences["only_departure_fr"]
            ])

            wrong_sentences.extend([
                self.create_object_text_label(
                    sentence, departure, arrival, prefix[0], "",
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
                    sentence, departure, arrival, prefix[1], "",
                    0, 1, 1, 0
                )
                for sentence in self.wrong_sentences["only_departure_en"]
            ])

            wrong_sentences.extend([
                self.create_object_text_label(
                    sentence, departure, arrival, prefix[1], "",
                    0, 1, 1, 0
                )
                for sentence in self.wrong_sentences["only_arrival_en"]
            ])

        return (
            correct_sentences +
            unclassified_sentences +
            np.random.choice(wrong_sentences, len(correct_sentences) - len(unclassified_sentences)).tolist()
        )

    @staticmethod
    def generate_text_classification_unknown_sentences(number: int) -> list:
        length = np.random.randint(16, 128)

        sentences = []

        for _ in range(number):
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

        data.extend(self.fill_text_classification_sentences_templates(departure.title(), arrival.title()))
        data.extend(self.fill_text_classification_sentences_templates(departure.lower(), arrival.lower()))

        length = int(len(data) / 4)

        # Get as much random sentences as there are sentences in the dataset
        data.extend(np.random.choice(self.random_sentences, length))

        # Generate unknown sentences
        data.extend(self.generate_text_classification_unknown_sentences(length))
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

    def generate_ner_tags_from_random_sentence(self) -> list:
        sentence = np.random.choice(self.random_sentences_french)["text"]
        formatted_sentence, _ = self.format_sentence_token_classification(sentence)
        tags_sentence = [self.ner_labels.index("O")] * (len(formatted_sentence))
        return [{
            "text": sentence,
            "tokens": formatted_sentence,
            "ner_tags": tags_sentence,
        }]

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

        for departure in self.cities:
            arrival = np.random.choice(self.cities)
            dataset.extend(self.get_text_classification_batch_sentences(departure, arrival))

            for special_char in ["-"]:
                if special_char in departure:
                    dataset.extend(self.get_text_classification_batch_sentences(departure.replace(special_char, " "), arrival))

        df = pd.DataFrame(dataset)

        # Shuffle dataset since random sentences at the end weight more in file size
        df = df.sample(frac=1).reset_index(drop=True)

        number_files = 4
        for id, df_i in enumerate(np.array_split(df, number_files)):
            df_i.to_csv(f"{path}dataset_text_classification_{id + 1}.csv", index=False, sep=";")

        print(f"Dataset generated with {len(dataset)} sentences.")

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

        for departure in self.cities:
            steps = {"departure": departure, "arrival": np.random.choice(self.cities)}

            for k, step in steps.items():
                steps[k] = step.title()
            dataset.extend(self.generate_ner_tags_from_correct_sentences(steps, sentences))

            for k, step in steps.items():
                steps[k] = step.lower()
            dataset.extend(self.generate_ner_tags_from_correct_sentences(steps, sentences))

            for k, step in steps.items():
                steps[k] = step.replace("-", " ")
            dataset.extend(self.generate_ner_tags_from_correct_sentences(steps, sentences))

        for _ in range(len(dataset)):
            dataset.extend(self.generate_ner_tags_from_random_sentence())

        df = pd.DataFrame(dataset)

        # Shuffle dataset since random sentences at the end weight more in file size
        df = df.sample(frac=1).reset_index(drop=True)

        number_files = 4
        for id, df_i in enumerate(np.array_split(df, number_files)):
            df_i.to_csv(f"{path}dataset_token_classification_{id + 1}.csv", index=False, sep=";")

        print(f"Dataset generated with {len(dataset)} sentences.")


if __name__ == "__main__":
    generator = DatasetGenerator()
    #generator.generate_text_classification_dataset(True)
    generator.generate_token_classification_dataset(True)
