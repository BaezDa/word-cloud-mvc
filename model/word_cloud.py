from wordcloud import WordCloud

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

import matplotlib.pyplot as plt

class WordCloudI():
    """Clase auxiliar para generar la nube de palabras.
    
    Contiene lo necesario para generar la nube
    de palabras.
    """
    def __init__(self, text, max_words = 40):
        self.text = text
        self.max_words = max_words
        self.stop_words = set(stopwords.words('spanish'))
        self.stop_words.update(["t", "co", "https", "t co", "https://t.co/", "pack", "LunesDeGanarSeguidores FelizLunes", "SabadoDeGanarSeguidores FelizSabado", "MiercolesDeGanarSeguidores FelizMiercoles", "DomingoDeGanarSeguidores FelizDomingo", "ViernesDeGanarSeguidores FelizViernes", "ven", "Feliz lunes", "persona", "Premium up", "quiero", "FelizDomingo"])
    
    def generate_word_cloud(self):
        return WordCloud(background_color='white', stopwords=self.stop_words, max_words=self.max_words).generate(self.text)