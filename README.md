# Parcs Afrique SQLPark

Ce projet permet de visualiser la distribution des parcs en Afrique et de générer des visualisations à partir des données fournies.

## Prérequis

- **Python 3.7 ou supérieur**
- **Git**
- **pip** (gestionnaire de paquets Python)

## Instructions

Suivez les étapes ci-dessous pour exécuter le code :

### 1. Cloner le dépôt ou télécharger le fichier principal

#### Option 1 : Cloner tout le dépôt

Pour récupérer tous les fichiers nécessaires :
```bash
git clone https://github.com/fasise/parcs_afrique_sqlpark.git
cd parcs_afrique_sqlpark
```

#### Option 2 : Télécharger uniquement le fichier `main.py`

Récupérez le fichier principal directement :

1. Allez sur [main.py](https://github.com/fasise/parcs_afrique_sqlpark/blob/main/main.py).
2. Téléchargez-le dans un répertoire de votre choix.

### 2. Créer et activer un environnement virtuel

#### Sous Windows
```bash
python -m venv env
env\Scripts\activate
```

#### Sous macOS/Linux
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Installer les dépendances

Si vous avez cloné le dépôt, utilisez le fichier `requirements.txt` pour installer toutes les bibliothèques nécessaires :
```bash
pip install -r requirements.txt
```

Si vous avez seulement téléchargé `main.py`, assurez-vous d'installer manuellement les bibliothèques requises (mentionnées dans le fichier ou lors de l'exécution).

### 4. Exécuter le programme

Une fois les bibliothèques installées, lancez le programme :
```bash
python main.py
```

Le programme va :
- Créer des fichiers de sortie contenant des données analysées.
- Générer des images pour visualiser les données.
- Produire un fichier HTML pour voir la distribution des parcs.

### 5. Visualiser les résultats

- **HTML** : Ouvrez le fichier HTML généré dans votre navigateur pour voir la distribution des parcs.
- **Images** : Regardez les fichiers image générés pour explorer les visualisations.

## Commandes récapitulatives

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/fasise/parcs_afrique_sqlpark.git
   cd parcs_afrique_sqlpark
   ```
2. Créer un environnement virtuel et l'activer :
   - Windows :
     ```bash
     python -m venv env
     env\Scripts\activate
     ```
   - macOS/Linux :
     ```bash
     python3 -m venv env
     source env/bin/activate
     ```
3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Exécuter le code :
   ```bash
   python main.py
   ```
5. Visualiser les résultats dans le navigateur ou à l'aide d'un logiciel d'affichage d'images.

## Liens utiles

- [Dépôt GitHub](https://github.com/fasise/parcs_afrique_sqlpark)
- [Fichier main.py](https://github.com/fasise/parcs_afrique_sqlpark/blob/main/main.py)

---

Si vous avez des questions, n'hésitez pas à ouvrir une issue dans le dépôt GitHub.
