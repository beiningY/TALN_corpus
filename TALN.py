from lxml import etree
from fpdf import FPDF
import os


class TALN_Corpus:
    # Initialiser la classe et analyser le fichier XML
    # Entrée : fichier_xml - chemin du fichier XML à analyse
    def __init__(self, fichier_xml):
        self.tree = etree.parse(fichier_xml)
        self.root = self.tree.getroot()
        self.dict = self.analyze()


    # Analyser les articles dans le fichier XML
    # Sortie : Retourne une liste de dictionnaires contenant les données des articles
    def analyze(self):
        data_dict = []
        namespace = {"teiCorpus": "http://www.tei-c.org/ns/1.0"}
        all_article = self.root.findall('.//teiCorpus:TEI', namespace)
        for article in all_article:
            data_temp = {}
            # abstract
            abstract = article.find(".//teiCorpus:div[@type='abstract']", namespace)
            data_temp['abstract'] = abstract.find(".//teiCorpus:p", namespace).text.strip()
            # keywords
            keywords = article.find(".//teiCorpus:div[@type='keywords']", namespace)
            data_temp['keywords'] = keywords.find(".//teiCorpus:p", namespace).text.strip().split(",")
            # content
            content = article.find(".//teiCorpus:body", namespace)
            data_temp['article'] = self.extract_text(content)
            data_dict.append(data_temp)
            # year
            date = article.find(".//teiCorpus:publicationStmt", namespace).find(".//teiCorpus:date", namespace)
            data_temp['year'] = date.text.strip()
        return data_dict
    
    # Extraire le texte d'un élément XML
    def extract_text(self, element):
        text = element.text if element.text else ''
        for child in element.getchildren():
            text += self.extract_text(child)
        return text

    # Générer un résumé de tous les articles en format texte ou PDF
    # Entrée : mode - 'text' pour un fichier texte, 'pdf' pour un fichier PDF
    def generate_abstract(self, mode):
        abstract = ""
        for data in self.dict:
            if data['abstract'] != 'None':
                abstract += data['abstract']
                abstract += "\n\n"
        if mode == 'text':
            self.write_txt('abstract.txt', abstract)
        elif mode == 'pdf':
            self.write_pdf('abstract.pdf', abstract)

    # Générer tous les articles en format texte ou PDF
    # Entrée : mode - 'text' pour un fichier texte, 'pdf' pour un fichier PDF
    def generate_all_articles(self, mode):
        if not os.path.exists("articles"):
            os.makedirs("articles")
        for index, article in enumerate(self.dict):
            file_name = os.path.join("articles", f"contenu_article_{index}")
            if mode == 'text':
                self.write_txt(f"{file_name}.txt", article['article'])
            elif mode == 'pdf':
                self.write_pdf(f"{file_name}.pdf", article['article'])

    # Trouver des articles par année et générer un fichier texte ou PDF
    # Entrée : year - l'année de publication des articles à trouver
    # mode - 'text' pour un fichier texte, 'pdf' pour un fichier PDF
    def find_by_year(self, year, mode):
        articles = ""
        if not isinstance(year, str):
            year = str(year)
        for data in self.dict:
            if data['year'] == year:
                articles += data['article']
                articles += "\n\n\n"
        if mode == 'text':
            self.write_txt('article_by_{}.txt'.format(year), articles)
        elif mode == 'pdf':
            self.write_pdf('article_by_{}.pdf'.format(year), articles)

    # Trouver des articles par mot-clé et générer un fichier texte ou PDF
    # Entrée : keyword - le mot-clé pour la recherche des articles
    # mode - 'text' pour un fichier texte, 'pdf' pour un fichier PDF
    def find_by_keyword(self, keyword, mode):
        articles = ""
        for data in self.dict:
            if keyword in data['keywords']:
                articles += data['article']
                articles += "\n\n\n"
        if mode == 'text':
            self.write_txt('article_by_{}.txt'.format(keyword), articles)
        elif mode == 'pdf':
            self.write_pdf('article_by_{}.pdf'.format(keyword), articles)

    def write_txt(self, name, data):
        with open(name, "w", encoding='utf8') as f:
            f.write(data)

    def write_pdf(self, name, data):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=data.encode('latin-1', 'replace').decode('latin-1'))
        pdf.output(name)


corpus = TALN_Corpus("corpus_taln_v1.tei.xml")
corpus.generate_abstract('pdf')
corpus.find_by_keyword('entité nommée','text')
corpus.find_by_year(1998,'text')
