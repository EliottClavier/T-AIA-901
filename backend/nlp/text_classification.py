from transformers import pipeline


class TextClassifier:

    model_name = "EliottClavier/distilbert-finetuned-text-classification-trip"

    classifier = None

    def __init__(self):
        self.classifier = pipeline(
            "text-classification",
            model=self.model_name
        )

    def predict(self, sentence, with_id=False):
        outputs = self.classifier(sentence["text"])
        if with_id:
            return f"{sentence['id']},{outputs[0]['label']}"
        return outputs[0]["label"]
