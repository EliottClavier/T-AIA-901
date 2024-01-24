import os
import random

import pandas as pd
import numpy as np

from dataset_generator import DatasetGenerator


class TextClassificationGenerator(DatasetGenerator):

    def create_object_text_label(self, sentence: str, departure: str, arrival: str, prefix: str, name: str, correct: int,
                                 not_french: int, not_trip: int, unknown: int) -> dict:

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

        sentence = self.replace_de_with_d(sentence, f_dict)

        return {
            "text": sentence.format(**f_dict),
            "CORRECT": correct,
            "NOT_FRENCH": not_french,
            "NOT_TRIP": not_trip,
            "UNKNOWN": unknown
        }

    def fill_sentences_templates(self, departure: str, arrival: str) -> list:

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

            random_names = np.random.choice(self.names, len(self.correct_sentences_with_names))
            correct_sentences.extend([
                self.create_object_text_label(
                    sentence, departure, arrival, prefix[0], random_names[i],
                    1, 0, 0, 0
                )
                for i, sentence in enumerate(self.correct_sentences_with_names)
            ])

            correct_sentences.extend([
                self.create_object_text_label(
                    sentence, departure, arrival, "", "",
                    1, 0, 0, 0
                )
                for sentence in self.correct_sentences_no_prefix
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
    def generate_unknown_sentences(number: int) -> list:
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

    def get_batch_sentences(self, departure: str, arrival: str) -> list:
        data = []

        for case in self.cases:
            for special_char in [""] + self.special_chars:
                m_departure = getattr(departure, case)()
                m_arrival = getattr(arrival, case)()

                if special_char and special_char in m_departure:
                    m_departure = m_departure.replace(special_char, " ")
                if special_char and special_char in m_arrival:
                    m_arrival = m_arrival.replace(special_char, " ")

                data.extend(self.fill_sentences_templates(m_departure, m_arrival))

        return data

    def generate(self, regenerate: bool = False) -> None:
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

        for i, departure in enumerate(self.departures):
            # pick random arrival and remove it from list
            arrival = np.random.choice(arrivals)
            arrivals.remove(arrival)
            dataset.extend(self.get_batch_sentences(departure, arrival))
            print(f"Progress: {i + 1}/{len(self.departures)}", end="\r")

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
        unknown_sentences = self.generate_unknown_sentences(length)
        df = pd.concat([df, pd.DataFrame(random_sentences), pd.DataFrame(unknown_sentences)])

        # Delete duplicates again on text column
        df = df.drop_duplicates(subset=["text"])

        # Shuffle dataset since random sentences at the end weight more in file size
        df = df.sample(frac=1).reset_index(drop=True)

        number_files = 4
        for id, df_i in enumerate(np.array_split(df, number_files)):
            df_i.to_csv(f"{path}dataset_text_classification_{id + 1}.csv", index=False, sep=";")

        print(f"Dataset generated with {len(df)} sentences.")


if __name__ == "__main__":
    token_classification_generator = TextClassificationGenerator()
    token_classification_generator.generate(True)
