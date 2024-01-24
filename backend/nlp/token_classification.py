from transformers import pipeline


class TokenClassifier:

    model_name = "EliottClavier/distilbert-finetuned-token-classification-ner-trip"

    classifier = None

    def __init__(self):
        self.classifier = pipeline(
            "token-classification",
            model=self.model_name,
            aggregation_strategy="simple"
        )

    @staticmethod
    def gather_outputs(outputs: list) -> list:
        # Group entities by their sequence
        grouped_entities = []
        current_group = []
        for entity in outputs:
            if not current_group or entity['start'] == current_group[-1]['end']:
                current_group.append(entity)
            else:
                grouped_entities.append(current_group)
                current_group = [entity]

        # Append the last group
        if current_group:
            grouped_entities.append(current_group)

        return grouped_entities

    def transform_sentence_from_outputs(self, sentence: str, outputs: list) -> list:
        groups = self.gather_outputs(outputs)
        locations = [{"label": group[0]["entity_group"], "city": sentence["text"][group[0]["start"]:group[-1]["end"]]}
                     for group in groups]
        sentence = {
            "id": str(sentence["id"]),
            "locations": locations
        }

        sentence["locations"] = sorted(sentence["locations"], key=lambda group: group["label"], reverse=True)
        return sentence

    @staticmethod
    def format_sentence_output(sentence_output: list) -> str:
        return f"{sentence_output['id']},{','.join([location['city'] for location in sentence_output['locations']])}"

    def predict(self, sentence):
        outputs = self.classifier(sentence["text"])
        outputs = self.format_sentence_output(self.transform_sentence_from_outputs(sentence, outputs))
        return outputs
