# Mobile

## Installation

Afin de pouvoir lancer l'application mobile, il vous faudra installer [Android Studio](https://developer.android.com/studio) et [Flutter](https://flutter.dev/docs/get-started/install).
Sur Android Studio, il vous faudra installer le SDK Android (API 29 minimum) et le plugin Dart et Flutter.

Pour vérifier l'installation de Flutter, exécutez la commande suivante :

```powershell
flutter doctor
```

Une fois l'installation de flutter validée, il faut installer les dépendances du projet, en exécutant la commande suivante dans le répertoire racine du projet :

```powershell
flutter pub get
```

## Lancement

Selon l'environnement de développement, il est possible de lancer l'application mobile sur un émulateur ou un appareil physique.

### Émulateur

Pour lancer l'application sur un émulateur, il faut d'abord le créer. Pour cela, il faut ouvrir Android Studio et cliquer sur `Tools > AVD Manager`. Ensuite, il faut cliquer sur `Create Virtual Device...` et choisir un appareil. Il est conseillé de choisir un appareil avec une version d'Android récente (API 29 minimum).

Une fois l'émulateur créé, il faut le lancer en cliquant sur `Tools > AVD Manager` puis sur le bouton `Play` à droite de l'émulateur.

Lorsque l'émulateur est lancé, il faut également executer la commande suivante pour activer le micro de l'émulateur:
```powershell
adb emu avd hostmicon
```

Pour finaliser la configuration du micro de l'émulateur, il faut également aller dans les options de l'émulateur et activer le micro
dans `Extended controls > Microphone` disponible lorsque l'émulateur est lancé.

Avant de lancer l'application sur l'émulateur, il faut modifier le fichier `lib/config.json` et remplacer la valeur de `API_URL` par:
```powershell
http://10.0.2.2:PORT
```

Enfin, pour lancer l'application sur l'émulateur, il faut exécuter la commande suivante dans le répertoire racine du projet :

```powershell
flutter run
```
ou utiliser le bouton `Run` dans Android Studio.

__Il est important de noter qu'il faut activer le micro de l'émulateur pour pouvoir utiliser la fonctionnalité de Speech-To-Text de l'application.__

### Appareil physique

Pour lancer l'application sur un appareil physique, il faut d'abord activer le mode développeur sur l'appareil. Pour cela, il faut suivre les instructions [suivantes](https://developer.android.com/studio/debug/dev-options).

Avant de lancer l'application, il faut modifier le fichier `lib/config.json` et remplacer la valeur de `API_URL` par l'adresse IP de l'ordinateur sur lequel est lancé le backend. Pour connaître l'adresse IP de l'ordinateur, il faut exécuter la commande suivante dans un terminal :

```powershell
ipconfig
```
et récupérer la valeur de `Adresse IPv4`.

La valeur de `API_URL` doit être de la forme suivante :
```powershell
http://IP:PORT
```

Ensuite, il faut connecter l'appareil à l'ordinateur et exécuter la commande suivante dans le répertoire racine du projet :

```powershell
flutter run
```
ou utiliser le bouton `Run` dans Android Studio.

