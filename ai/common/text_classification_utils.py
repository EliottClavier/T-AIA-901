import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
from sklearn.model_selection import train_test_split, KFold
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.utils import shuffle

# Notebooks imports
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.svm import LinearSVC


# Cell 1
def load_dataset():
    path = "data/text_classification/"
    dataset = pd.DataFrame()
    for file in os.listdir(path):
        if file.endswith(".csv"):
            new_data = pd.read_csv(os.path.join(path, file), sep=";")
            dataset = pd.concat([dataset, new_data], ignore_index=True)
    return dataset


# Cell 2
def prepare_labels(dataset):
    labels = [label for label in dataset.columns if label != 'text']
    id2label = {i: label for i, label in enumerate(labels)}
    label2id = {v: k for k, v in id2label.items()}
    print(labels)
    return labels, id2label, label2id


# Cell 3
def show_labels_distribution(dataset, labels):
    plt.bar(labels, [sum(dataset[label]) for label in labels])
    plt.show()


def flatten_trips_labels(dataset):
    num_main = dataset['CORRECT'].sum()

    # Filtrage des données où NOT_TRIP est égal à 1
    remove = dataset[dataset['NOT_TRIP'] == 1]

    # Mélange et sélection des données à conserver
    remove_to_keep = shuffle(remove, random_state=42).head(num_main)

    # Filtrage des données où NOT_TRIP est égal à 0
    dataset = dataset[dataset['NOT_TRIP'] == 0]

    # Concaténation des datasets
    return pd.concat([dataset, remove_to_keep], ignore_index=True)


# Cell 4
def split_dataset(dataset, labels, final_dataset_size=0.3, test_size=0.2, val_size=0.5, random_state=0):
    # Réduction de la taille du dataset si nécessaire
    dataset = dataset.sample(frac=1-final_dataset_size, random_state=random_state)

    # Séparation du dataset en train et reste (test + validation)
    X_train, X_rest, y_train, y_rest = train_test_split(
        dataset['text'], dataset[labels], test_size=test_size, random_state=random_state
    )

    # Calcul de la taille de validation par rapport à la taille du reste (test + validation)
    val_size_relative = val_size / (test_size + val_size)

    # Séparation du reste en test et validation
    X_test, X_val, y_test, y_val = train_test_split(
        X_rest, y_rest, test_size=val_size_relative, random_state=random_state
    )

    return X_train, X_test, X_val, y_train, y_test, y_val


# Cell 6
def create_pipeline(vectorizer,
                    classifier,
                    **pipeline_args):
    return Pipeline([('vectorizer', vectorizer), ('classifier', OneVsRestClassifier(classifier))], **pipeline_args)


def evaluate_model_kfold_with_predictions(pipeline,
                                          dataset,
                                          labels,
                                          id2label,
                                          n_splits=5,
                                          random_state=0):
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    X = dataset['text']
    y = dataset[labels]

    for fold, (train_index, test_index) in enumerate(kf.split(X)):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        show_classification_report(y_pred, y_test, labels, id2label)
        show_confusion_matrix(y_pred, y_test, labels, id2label)
        show_roc_curves(labels, y_pred, y_test, id2label)

        show_samples_predictions(pipeline, id2label)


# Cell 7
def show_classification_report(y_pred, y_test, labels, pipeline_label=""):
    print(f"Classification Report for {pipeline_label}")
    print(classification_report(y_test, y_pred, target_names=labels))


# Cell 8
def get_confusion_matrix(y_pred, y_test):
    return confusion_matrix(y_test.values.argmax(axis=1), y_pred.argmax(axis=1))


def show_confusion_matrix(y_pred, y_test, labels, pipeline_label=""):
    cm = get_confusion_matrix(y_pred, y_test)
    sns.heatmap(cm, annot=True, cmap='Blues', fmt='g', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title(f'{pipeline_label} Confusion Matrix')
    plt.show()


# Cell 9
def show_roc_curves(labels, y_pred, y_test, pipeline_label=""):
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    for i in range(len(labels)):
        fpr[i], tpr[i], _ = roc_curve(y_test.values[:, i], y_pred[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    plt.figure(figsize=(10, 10))

    for i in range(len(labels)):
        plt.plot(fpr[i], tpr[i], label=f"{labels[i]} (AUC = {roc_auc[i]:.2f})")

    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'{pipeline_label} ROC Curves')
    plt.legend()
    plt.show()


# Cell 10
def show_samples_predictions(pipeline, id2label):
    texts = [
        "Je veux aller de Port-Boulet à Le Havre.",
        "Je veux aller de Port-Boulet au Havre.",
        "Je vais de Nantes à Paris.",
        "Je vais de Nantes à Nantes.",
        "Je veux aller de Nantes à Nantes.",
        "Je vais à Port-Boulet en partant de Le Havre",
        "Je vais à Port-Boulet en partant du Havre",
        "Peux-tu m'aider à trouver mon chemin vers Paris en partant d'Épierre ?",
        "Je cherche un moyen d'aller de Margny-Lès-Compiègne à Saarbrücken /Sarrebruck.",
        "Je veux me rendre chez mon ami Etienne à Saint-Étienne depuis Nantes.",
        "Je veux aller de la ville de Marseille à Tours.",
        "Recherche le chemin le plus court entre la ville de Lorient et Paris",
        "Trouve-moi un itinéraire pour aller à Besançon depuis la ville d'Oyonnax.",
        "Ca met combien de temps un Toulouse Paris ?",
        "C'est quoi le trajet de Troyes à Niort ?",
        "Comment aller à Niort depuis Troyes ?",
        "Comment aller à Niort depuis Troyes",
        "Recherche un itinéraire de Nantes à Paris où habite Théo",
        "Trouve-moi le chemin le plus rapide vers Paris depuis Nantes pour arriver chez Michel.",
        "Il y a-t-il des trains de Nantes à Montaigu"
    ]

    predicted_labels = pipeline.predict(texts)

    predicted_proba = pipeline.predict_proba(texts)

    # Displaying the predicted labels and probability scores for new texts
    for text, p_labels, prob in zip(texts, predicted_labels, predicted_proba):
        print("*", text)
        for i, score in enumerate(prob):
            print(' -', id2label[i], '=>', f"{round(score * 100, 1)}%")
        print()
