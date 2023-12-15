# TALN.py Analyseur de Corpus XML pour TALN

Ce programme est utilisé pour analyser des fichiers XML et en extraire des données.

## Dépendances

- Python 3.x
- Bibliothèque lxml
- Bibliothèque fpdf

## Utilisation

1. Assurez-vous d'avoir Python 3.x installé.
2. Installez les dépendances requises : lxml et fpdf.
   - Utilisez pip install lxml pour installer la bibliothèque lxml.
   - Utilisez pip install fpdf pour installer la bibliothèque fpdf.
3. Placez le fichier XML que vous souhaitez analyser dans le même répertoire que le fichier de code et nommez-le "corpus_taln_v1.tei.xml" (ou modifiez le nom du fichier dans le code si nécessaire).
4. Exécutez le fichier de code.

## Fonctionnalités

- `TALN_Corpus` classe: Utilisée pour analyser le fichier XML et extraire des données.
    - `__init__(self, fichier_xml)`: Fonction d'initialisation qui prend un paramètre fichier_xml représentant le chemin du fichier XML à analyser.
    - `analyze(self)`: Analyse le fichier XML et retourne un dictionnaire de données.
    - `extract_text(self, element)`: Fonction auxiliaire qui extrait de manière récursive le contenu textuel des éléments XML.
    - `generate_abstract(self, mode)`: Extrait tous les résumés et génère un fichier texte ou PDF.
    - `generate_all_articles(self, mode)`: Générer tous les articles en format texte ou PDF.
    - `find_by_year(self, year, mode)`: Trouve des articles par année et génère un fichier texte ou PDF contenant les articles correspondants.
    - `find_by_keyword(self, keyword, mode)`: Trouve des articles par mot-clé et génère un fichier texte ou PDF contenant les articles correspondants.
    - `write_txt(self, name, data)`: Écrit les données dans un fichier texte.
    - `write_pdf(self, name, data)`: Écrit les données dans un fichier PDF.

## Exemple d'utilisation

python
from lxml import etree
from fpdf import FPDF
import xml

#Créer un objet TALN_Corpus et fournir le chemin du fichier XML à analyser
corpus = TALN_Corpus("corpus_taln_v1.tei.xml")

#Générer un fichier PDF contenant tous les résumés
corpus.generate_abstract('pdf')

#Trouver et générer un fichier texte contenant des articles pour un mot-clé spécifique
corpus.find_by_keyword('entité nommée', 'text')

#Trouver et générer un fichier texte contenant des articles pour une année spécifique
corpus.find_by_year(1998, 'text')



# Kmeans.py Analyseur de Texte et Clustering avec NLTK et K-means

Ce programme est conçu pour traiter des documents textuels et appliquer une technique de clustering pour les regrouper en catégories.

## Dépendances

- Python 3.x
- Bibliothèques NLTK, scikit-learn et Matplotlib
- Bibliothèque NumPy

## Installation

1. Assurez-vous d'avoir Python 3.x installé.
2. Installez les bibliothèques nécessaires :
   - NLTK : pip install nltk
   - scikit-learn : pip install scikit-learn
   - Matplotlib : pip install matplotlib
   - NumPy : pip install numpy

## Utilisation

1. Placez les fichiers texte à analyser dans un dossier.
2. Ajustez le chemin du dossier dans le paramètre folder_path de la classe KMeansTextCluster.
3. Exécutez le script.

## Fonctionnalités

- `textNLTK` classe: Utilisée pour le prétraitement de texte.
- `KMeansTextCluster` classe: Applique l'algorithme de clustering K-means aux textes prétraités.
    - `process_documents(self)`: Traite chaque fichier texte dans le dossier spécifié.
    - `print_clusters(self)`: Affiche le cluster assigné à chaque document.
    - `cluster_documents(self)`: Exécute l'algorithme K-means sur les documents.
    - `visualize_clusters(self)`: Visualise les résultats du clustering.


## Exemple d'utilisation

folder_path = 'articles' 
kmeans_cluster = KMeansTextCluster(folder_path, num_clusters=3)
kmeans_cluster.process_documents()
kmeans_cluster.cluster_documents()
kmeans_cluster.print_clusters()
kmeans_cluster.visualize_clusters()
