# Expérimentations IA
Les expérimentations IA sont divisées en deux parties :
- [text-classification](text-classification) : classification de texte avec des algorithmes de machine learning et des transformers
- [token-classification](token-classification) : NER avec des transformers

## Installation
Dans le répertoire racine du projet, exécutez la suite de commandes qui suit, en notant qu'il est recommandé d'utiliser [Python 3.11.5](https://www.python.org/downloads/release/python-3115/).

Créer un environnement virtuel avec la commande suivante :
```powershell
python -m venv env
```
Puis activer l'environnement virtuel :
```powershell
env\Scripts\activate
```
Enfin, installer les dépendances :
```powershell
pip install -r requirements.txt
```

Il vous faudra également installer __pytorch__ [selon votre configuration](https://pytorch.org/get-started/locally/). La commande par défaut est la suivante :
```powershell
pip install torch torchvision torchaudio
```

__La version vérifiée de pytorch pour ce projet est la 2.1.2.__

## Lancement de Jupyter Notebook
Dans le répertoire racine du projet, exécutez la commande suivante :
```powershell
jupyter notebook
```
Une page web s'ouvrira dans votre navigateur. Vous pourrez alors naviguer dans les différents répertoires et ouvrir les notebooks pour les consulter ou les exécuter.