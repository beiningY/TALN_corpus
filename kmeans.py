import os
from nltk import*
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

# La classe textNLTK pour le pré-traitement de texte.
class textNLTK:
    def __init__(self, fichier, encoding="utf-8"):
        self._fichier = fichier
        self._encoding = encoding
        self._content = []
        self._tokens = []
        self._listWords = []
        self._listStems = []
        try:
            with open(self._fichier, encoding=self._encoding, mode='r') as f:
                lines = f.readlines()
                for line in lines:
                    lig = line.strip()
                    self._content.append(lig)
            self._length = len(self._content)
        except OSError as err:
            print("Erreur OS: {0}".format(err))

    def token(self):
        for phrase in self._content:
            self._tokens.extend(word_tokenize(phrase, language='french'))

    def stopwords(self):
        stopWords = set(stopwords.words('french'))
        self._listWords = [token for token in self._tokens if token.lower() not in stopWords]
        return self._listWords

    def stopwords_and_stem(self):
        stemmer = SnowballStemmer("french")
        self._listStems = [stemmer.stem(token) for token in self.stopwords()]
        return self._listStems
    
# Initialiser la classe pour le clustering de documents textuels.
class KMeansTextCluster:
    def __init__(self, folder_path, num_clusters=3):
        self.folder_path = folder_path
        self.num_clusters = num_clusters
        self.documents = []
        self.clusters = []

    # Parcourt le dossier spécifié, applique le traitement de texte sur chaque fichier(la tokenisation, l'élimination des mots vides et la racinisation).
    def process_documents(self):
        for filename in os.listdir(self.folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(self.folder_path, filename)
                text_processor = textNLTK(file_path)
                text_processor.token()
                processed_text = text_processor.stopwords_and_stem()
                self.documents.append(' '.join(processed_text))

    # Imprimer le cluster de chaque document.
    def print_clusters(self):
        for i, cluster in enumerate(self.clusters):
            print(f"L'article {i} a été classé dans le cluster {cluster}")


    def cluster_documents(self):
        # Créer un vectoriseur TF-IDF
        vectorizer = TfidfVectorizer()
        # Transformer les documents en représentation TF-IDF
        X = vectorizer.fit_transform(self.documents)
        km = KMeans(n_clusters=self.num_clusters)
        km.fit(X)
        self.clusters = km.labels_.tolist()
        # Réduction de dimension avec PCA pour la visualisation
        self.X_2d = PCA(n_components=2).fit_transform(X.toarray())

    # Visualiser les résultats de clustering.
    def visualize_clusters(self):
        plt.figure(figsize=(8, 6))
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        # Obtenir les points appartenant au cluster actuel
        for i in range(self.num_clusters):
            points = self.X_2d[np.array(self.clusters) == i]
            print(f"Cluster {i}: {len(points)} points") 
            # Dessiner le graphique à nuage de points
            plt.scatter(points[:, 0], points[:, 1], s=50, c=colors[i], label=f'Cluster {i}')
        plt.title("K-means Clustering Visualization")
        plt.legend()
        plt.show()

folder_path = 'articles' 
kmeans_cluster = KMeansTextCluster(folder_path, num_clusters=3)
kmeans_cluster.process_documents()
kmeans_cluster.cluster_documents()
kmeans_cluster.print_clusters()
kmeans_cluster.visualize_clusters()
