# Backend
Le backend est une application Flask qui va permettre de faire le lien entre l'application mobile et les modèles de machine learning.

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

## Lancement
Une fois l'environnement virtuel configuré, exécutez les commandes suivantes pour lancer l'application :

Si l'environnement virtuel n'est pas activé :
```powershell
env\Scripts\activate
```
Enfin, lancer l'application Flask avec la commande suivante :
```powershell
flask run --host 0.0.0.0
```

Le paramètre `--host 0.0.0.0` va permettre à l'application mobile connectée au même réseau local de pouvoir accéder à l'application Flask.

## Postman

Pour tester les routes de l'application Flask, vous pouvez utiliser [Postman](https://www.postman.com/downloads/) et importer la collection `postman_collection.json` qui se trouve à la racine du projet backend.