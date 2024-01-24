from .text_classification import TextClassifier
from .token_classification import TokenClassifier

text_classifier = TextClassifier()
token_classifier = TokenClassifier()


def generate_dict_from_sentences(sentences: list) -> list:
    return [
        {
            "id": parts[0],
            "text": parts[1]
        } for sentence in sentences if (parts := sentence.split(',')) and len(parts) > 1
    ]


def process_classification(sentences: list, classifier_func, options=None):
    results = []
    for sentence in generate_dict_from_sentences(sentences):
        results.append(classifier_func(sentence, **options if options else {}))
    return '\n'.join(results)


def process_text_classification(sentences: list):
    return process_classification(sentences, text_classifier.predict, {"with_id": True})


def process_token_classification(sentences: list):
    return process_classification(sentences, token_classifier.predict)


def process_nlp(sentences: list):
    def nlp_classifier(sentence):
        text_label = text_classifier.predict(sentence)
        return token_classifier.predict(sentence) if text_label == "CORRECT" else f"{sentence['id']},{text_label}"

    return process_classification(sentences, nlp_classifier)
