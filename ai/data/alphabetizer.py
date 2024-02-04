def trier_phrases(fichier_source, fichier_destination):
    with open(fichier_source, 'r', encoding='utf-8') as fichier:
        phrases = fichier.readlines()

    phrases_triees = sorted(phrases, key=lambda s: s.strip().lower())

    with open(fichier_destination, 'w', encoding='utf-8') as fichier:
        for phrase in phrases_triees:
            fichier.write(phrase)


if __name__ == '__main__':
    import sys
    trier_phrases(sys.argv[1], sys.argv[2])