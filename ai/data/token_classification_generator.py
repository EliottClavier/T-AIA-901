import os
import re

import pandas as pd
import numpy as np

from dataset_generator import DatasetGenerator


def flatten_list(nested_list):
    flattened_list = []
    for i in nested_list:
        if isinstance(i, list):
            flattened_list.extend(flatten_list(i))
        else:
            flattened_list.append(i)
    return flattened_list


class TokenClassificationGenerator(DatasetGenerator):

    @staticmethod
    def split_sentence(sentence: str) -> list:
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
    def format_sentence(cls, sentence: str) -> tuple[list, bool]:
        formatted_sentence = cls.split_sentence(sentence)
        sentence, should_add_dot = cls.manage_trailing_punctuation(formatted_sentence)
        return sentence, should_add_dot

    def prepare_sentence_common(self, final_sentences: list, sentence: str) -> None:
        final_sentences.append(sentence.format(departure="{departure}", arrival="{arrival}", name="{name}"))
        if sentence[-1] in ["."]:
            final_sentences.append(sentence.format(departure="{departure}", arrival="{arrival}", name="{name}")[:-1])
        elif sentence[-1] in ["?", "!"]:
            final_sentences.append(sentence.format(departure="{departure}", arrival="{arrival}", name="{name}")[:-2])

    def prepare_sentences(self) -> list:
        final_sentences = []

        for sentence in self.correct_sentences + self.correct_sentences_with_names:
            self.prepare_sentence_common(final_sentences, sentence)

            random_fr_prefix = np.random.choice(self.fr_prefixes)

            final_sentences.append(np.random.choice([
                sentence.format(departure=random_fr_prefix + "{departure}", arrival="{arrival}", name="{name}"),
                sentence.format(departure="{departure}", arrival=random_fr_prefix + "{arrival}", name="{name}"),
                sentence.format(departure=random_fr_prefix + "{departure}", arrival=random_fr_prefix + "{arrival}", name="{name}")
            ]))

        for sentence in self.correct_sentences_no_prefix:
            self.prepare_sentence_common(final_sentences, sentence)

        return final_sentences

    def generate_bert_ner_tags_from_correct_sentences(self, steps: dict, sentences: list, random_names: list[str]) -> pd.DataFrame:
        data = []

        for x, sentence in enumerate(sentences):
            alt_sentence = sentence.replace("{", "").replace("}", "")
            formatted_sentence = self.split_sentence(alt_sentence)

            tags_sentence = [self.ner_labels.index("O")] * (len(formatted_sentence))

            for i, word in enumerate(formatted_sentence):
                if "departure" in word:
                    formatted_step = self.split_sentence(steps["departure"])
                    tags_sentence[i] = [self.ner_labels.index("B-DEP")] + [self.ner_labels.index("I-DEP")] * (len(formatted_step) - 1)

                if "arrival" in word:
                    formatted_step = self.split_sentence(steps["arrival"])
                    tags_sentence[i] = [self.ner_labels.index("B-ARR")] + [self.ner_labels.index("I-ARR")] * (len(formatted_step) - 1)

                if "name" in word:
                    formatted_name = self.split_sentence(random_names[x])
                    tags_sentence[i] = [self.ner_labels.index("O")] * len(formatted_name)

            # remove 2D list inside list
            tags_sentence = flatten_list(tags_sentence)

            final_sentence = self.replace_de_with_d(sentence, steps)
            final_sentence = final_sentence.format(departure=steps["departure"], arrival=steps["arrival"], name=random_names[x])

            formatted_final_sentence, should_add_dot = self.format_sentence(final_sentence)

            if should_add_dot:
                tags_sentence.append(self.ner_labels.index("O"))

            data.append({
                "text": final_sentence,
                "tokens": formatted_final_sentence,
                "ner_tags": tags_sentence,
            })

        return pd.DataFrame(data, columns=["text", "tokens", "ner_tags"])

    def generate_spacy_ner_tags_from_correct_sentences(self, steps: dict, sentences: list, random_names: list[str]) -> pd.DataFrame:
        data = []

        for i, sentence in enumerate(sentences):
            final_sentence = self.replace_de_with_d(sentence, steps)
            final_sentence = final_sentence.format(departure=steps["departure"], arrival=steps["arrival"], name=random_names[i])
            spacy_tags = []

            elements = ["departure", "arrival"]
            elements = sorted(elements, key=lambda x: sentence.find("{" + x + "}"))

            for step in elements:
                brackets = "{" + step + "}"
                index = sentence.find(brackets)

                if index != -1:
                    spacy_tags.append({"start": index, "end": index + len(steps[step]), "label": step[0:3].upper()})
                    sentence = sentence.replace(brackets, steps[step])

            data.append({
                "text": final_sentence,
                "spacy_ner_tags": spacy_tags,
            })
        return pd.DataFrame(data, columns=["text", "spacy_ner_tags"])

    def generate_ner_tags_from_correct_sentences(self, steps: dict, sentences: list) -> list:
        random_names = np.random.choice(self.names, len(sentences))
        bert_data = self.generate_bert_ner_tags_from_correct_sentences(steps, sentences, random_names)
        spacy_data = self.generate_spacy_ner_tags_from_correct_sentences(steps, sentences, random_names)

        # Combine both datasets based on text attribute of objects using pandas
        return pd.merge(bert_data, spacy_data, on="text").to_dict("records")

    def generate_ner_tags_from_random_sentences(self, random_sentences: list) -> list:
        for random_sentence in random_sentences:
            sentence = random_sentence["text"]
            formatted_sentence, _ = self.format_sentence(sentence)
            tags_sentence = [self.ner_labels.index("O")] * (len(formatted_sentence))
            random_sentence["tokens"] = formatted_sentence
            random_sentence["ner_tags"] = tags_sentence
        return random_sentences

    def generate(self, regenerate: bool = False) -> None:
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

        sentences = self.prepare_sentences()
        print(f"Generated {len(sentences)} sentences.")

        arrivals = self.arrivals.copy()

        for i, departure in enumerate(self.departures):
            arrival = np.random.choice(arrivals)
            arrivals.remove(arrival)
            steps = {"departure": departure, "arrival": arrival}

            for special_char in [""] + self.special_chars:
                for k, step in steps.items():
                    steps[k] = getattr(step, np.random.choice(self.cases))()

                    if special_char and special_char in step:
                        steps[k] = step.replace(special_char, " ")

                dataset.extend(self.generate_ner_tags_from_correct_sentences(steps, sentences))

            print(f"Progress: {i + 1}/{len(self.departures)}", end="\r")

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
    token_classification_generator = TokenClassificationGenerator()
    token_classification_generator.generate(True)
