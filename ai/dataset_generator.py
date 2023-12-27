import os
import pandas as pd
import numpy as np


class DatasetGenerator:

    cities = []
    random_sentences = []

    def __init__(self):
        self.load_cities()
        self.load_random_sentences()

    @staticmethod
    def fill_sentence(departure: str, arrival: str) -> list:
        correct_sentences = [
            # French templates
            {"text": f"Je veux aller de {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"J'aimerais me rendre de {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je prévois un voyage de {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je cherche un moyen d'aller de {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Mon trajet va de {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je suis en train de planifier un déplacement de {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Le voyage de {departure} à {arrival} est ce que je recherche.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Trouver un moyen d'atteindre {arrival} depuis {departure} est mon objectif.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Serait-il possible de me rendre de {departure} à {arrival}, s'il vous plaît ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je souhaiterais me déplacer de {departure} à {arrival}, si c'est réalisable.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Pourriez-vous m'indiquer comment aller de {departure} à {arrival}, je vous prie ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Allez de {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Dirigez-vous vers {arrival} en partant de {departure}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Trouve un moyen d'atteindre {arrival} depuis {departure}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Rendez-vous à {arrival} depuis {departure}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Partez pour {arrival} en partant de {departure}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"{departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"De {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"De {departure} vers {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Depuis {departure} vers {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Trouve-moi le chemin de {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Comment puis-je me rendre de {departure} à {arrival} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Indique-moi le trajet de {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Pourrais-tu m'aider à rejoindre {arrival} depuis {departure} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je souhaite aller de {departure} à {arrival}, s'il te plaît.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Peux-tu me guider de {departure} vers {arrival} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Trouve le meilleur itinéraire de {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Montre-moi le chemin pour passer de {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Pourrais-tu me donner les indications pour aller de {departure} à {arrival} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je voudrais savoir comment me rendre de {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Y a-t-il un moyen d'aller de {departure} à {arrival} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je recherche un itinéraire de {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Peux-tu me diriger vers {arrival} depuis {departure} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je désire aller de {departure} à {arrival}. Comment faire ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Pourrais-tu m'aider à planifier le trajet de {departure} vers {arrival} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Comment puis-je me rendre de {departure} à {arrival} le plus rapidement ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"J'aimerais connaître le chemin pour aller de {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Trouve-moi un moyen de transport de {departure} jusqu'à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Pourrais-tu me donner les indications pour rejoindre {arrival} depuis {departure} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je cherche à me déplacer de {departure} à {arrival}. Comment procéder ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Indique-moi le trajet le plus simple de {departure} vers {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 1},
            {"text": f"Je voudrais savoir comment me rendre de {departure} à {arrival}, s'il te plaît.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Peux-tu m'aider à trouver mon chemin de {departure} à {arrival} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Montre-moi le chemin pour me rendre de {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je souhaite aller à {arrival} en partant de {departure}. Comment faire ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Comment atteindre {arrival} à partir de {departure} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Pourrais-tu me guider vers {arrival} depuis {departure} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Trouve-moi un itinéraire pour aller de {departure} à {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je cherche à me déplacer de {departure} vers {arrival}. Peux-tu m'aider ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Comment puis-je rejoindre {arrival} depuis {departure} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je souhaite me rendre de {arrival} jusqu'à {departure}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Trouve-moi un itinéraire de {arrival} vers {departure}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Comment puis-je aller à {departure} en venant de {arrival} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Peux-tu me guider de {arrival} jusqu'à {departure} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je cherche le chemin pour aller à {departure} depuis {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Montre-moi le trajet pour aller à {departure} en partant de {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Pourrais-tu m'indiquer comment aller de {arrival} à {departure} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je voudrais savoir comment me rendre à {departure} depuis {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Y a-t-il un moyen d'atteindre {departure} depuis {arrival} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je recherche un itinéraire pour aller à {departure} en partant de {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Indique-moi le chemin depuis {arrival} jusqu'à {departure}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je souhaite me déplacer vers {departure} à partir de {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Pourrais-tu me diriger de {arrival} vers {departure} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Comment puis-je me rendre à {departure} en partant de {arrival} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je désire aller à {departure} depuis {arrival}. Peux-tu aider ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Peux-tu m'aider à planifier le trajet depuis {arrival} jusqu'à {departure} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Comment atteindre {departure} en partant de {arrival} le plus rapidement ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"J'aimerais connaître le chemin pour aller à {departure} depuis {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Trouve-moi un moyen de transport de {arrival} vers {departure}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je cherche à me déplacer vers {departure} depuis {arrival}. Comment procéder ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Indique-moi le trajet le plus simple depuis {arrival} vers {departure}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je voudrais savoir comment me rendre à {departure} depuis {arrival}, s'il te plaît.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Peux-tu m'aider à trouver mon chemin de {arrival} à {departure} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Montre-moi le chemin pour aller à {departure} à partir de {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je souhaite aller à {departure} en partant de {arrival}. Comment faire ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Comment atteindre {departure} depuis {arrival} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Pourrais-tu me guider vers {departure} depuis {arrival} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Trouve-moi un itinéraire pour aller à {departure} depuis {arrival}.", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Je cherche à me déplacer vers {departure} depuis {arrival}. Peux-tu m'aider ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Comment puis-je rejoindre {departure} à partir de {arrival} ?", "CORRECT": 1, "NOT_FRENCH": 0, "NOT_TRIP": 0, "UNKNOWN": 0},
        ]

        wrong_sentences = [
            # English equivalents
            {"text": f"I want to go from {departure} to {arrival}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"I would like to travel from {departure} to {arrival}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"I am planning a trip from {departure} to {arrival}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"I am looking for a way to go from {departure} to {arrival}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"My journey goes from {departure} to {arrival}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"I am in the process of planning a trip from {departure} to {arrival}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"The journey from {departure} to {arrival} is what I'm looking for.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Finding a way to reach {arrival} from {departure} is my goal.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Would it be possible for me to go from {departure} to {arrival}, please?", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"I would like to travel from {departure} to {arrival}, if it's possible.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Could you tell me how to get from {departure} to {arrival}, please?", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Go from {departure} to {arrival}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Head towards {arrival} from {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Find a way to reach {arrival} from {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Go to {arrival} from {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"Depart for {arrival} from {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},
            {"text": f"{departure} to {arrival}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 0, "UNKNOWN": 0},

            # Seulement le départ
            {"text": f"Je veux partir de {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Mon trajet commence à {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Dirigez-vous vers une autre ville à partir de {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Je cherche un moyen de partir de {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Trouve un moyen de quitter {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Rendez-vous quelque part en partant de {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Partez de {departure}, c'est le début de l'aventure.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Le départ de {departure} est imminent.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Je suis en train de planifier un départ de {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Allons ailleurs que {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},

            # Only departure
            {"text": f"I want to depart from {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"My journey starts at {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Head towards another city from {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"I'm looking for a way to depart from {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Find a way to leave {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Meet somewhere starting from {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Leave from {departure}, it's the beginning of the adventure.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"The departure from {departure} is imminent.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"I'm planning a departure from {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Let's go somewhere other than {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},

            # We use departure parameter as arrival
            # Seulement l'arrivée
            {"text": f"Je veux arriver à {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Mon trajet se termine à {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Dirigez-vous vers {departure} depuis une autre ville.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Je cherche un moyen d'arriver à {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Trouve un moyen d'atteindre {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Rendez-vous à {departure}, c'est ma destination.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Arrivez à {departure}, c'est là que je veux aller.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"L'arrivée à {departure} est prévue.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Je suis en train de planifier une arrivée à {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Allons vers {departure}, c'est là où je souhaite être.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},

            # Only arrival
            {"text": f"I want to arrive at {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"My journey ends at {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Head towards {departure} from another city.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"I'm looking for a way to arrive at {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Find a way to reach {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Meet at {departure}, it's my destination.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Arrive at {departure}, that's where I want to go.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"The arrival at {departure} is scheduled.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"I'm planning an arrival at {departure}.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Let's head towards {departure}, that's where I want to be.", "CORRECT": 0, "NOT_FRENCH": 1, "NOT_TRIP": 1, "UNKNOWN": 0}
        ]

        unclassified_sentences = [
            {"text": f"Je veux aller de {departure} à {arrival} ou {arrival}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Je veux me rendre de {departure} à {arrival} ou {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Je veux me rendre à {arrival} ou {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Je veux me diriger vers {arrival} depuis {departure} ou {arrival}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"Je veux aller à {arrival} depuis {departure} ou pourquoi pas {arrival}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"{departure} à {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"{departure} vers {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"{arrival} à {arrival}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"{arrival} vers {arrival}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"J'aimerais aller à {departure} en partant de {departure}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
            {"text": f"J'aimerais aller à {arrival} en partant de {arrival}.", "CORRECT": 0, "NOT_FRENCH": 0, "NOT_TRIP": 1, "UNKNOWN": 0},
        ]

        return (
            correct_sentences +
            unclassified_sentences +
            np.random.choice(wrong_sentences, len(correct_sentences) - len(unclassified_sentences)).tolist()
        )

    def load_cities(self):
        path = os.path.join(os.path.abspath(__file__), "..", "..", "backend", "path_finder", "data", "graph.json")
        df = pd.read_json(path)
        self.cities = list(df.keys())

    def load_random_sentences(self):
        # Dataset from https://www.kaggle.com/datasets/basilb2s/language-detection?resource=download
        path = os.path.join(os.path.abspath(__file__), "..", "data", "random_sentences.csv")
        df = pd.read_csv(path, sep=",")
        df["Language"] = df["Language"].apply(lambda x: 0 if x == "French" else 1)

        # create a list of sentences, with column Text to key text, and NOT_FRENCH to key Language
        # also set NOT_TRIP to 1, UNKNOWN to 0 and CORRECT to 0
        self.random_sentences = ((df[["Text", "Language"]]
                                 .rename(columns={"Text": "text", "Language": "NOT_FRENCH"}))
                                 .assign(NOT_TRIP=1, UNKNOWN=0, CORRECT=0).to_dict(orient="records"))

    @staticmethod
    def generate_unknown_sentences(number: int) -> list:
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

    def get_batch_sentences(self, departure: str, arrival: str) -> list:
        data = []

        data.extend(self.fill_sentence(departure.title(), arrival.title()))
        data.extend(self.fill_sentence(departure.lower(), arrival.lower()))

        length = int(len(data) / 4)

        # Get as much random sentences as there are sentences in the dataset
        data.extend(np.random.choice(self.random_sentences, length))

        # Generate unknown sentences
        data.extend(self.generate_unknown_sentences(length))
        return data

    def generate_text_classification_dataset(self, regenerate=False):
        print("Generating text classification dataset...")
        if os.path.exists("./data/dataset_text_classification.csv") and not regenerate:
            print("File already exists, skipping generation.")
            return

        dataset = []

        for departure in self.cities:
            arrival = np.random.choice(self.cities)
            dataset.extend(self.get_batch_sentences(departure, arrival))

            for special_char in ["-"]:
                if special_char in departure:
                    dataset.extend(self.get_batch_sentences(departure.replace(special_char, " "), arrival))

        df = pd.DataFrame(dataset)
        df.to_csv("data/dataset_text_classification.csv", index=False, sep=";")
        print(f"Dataset generated with {len(dataset)} sentences.")


if __name__ == "__main__":
    generator = DatasetGenerator()
    generator.generate_text_classification_dataset()