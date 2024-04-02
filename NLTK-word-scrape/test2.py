import re
import collections
import nltk
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt


def check_url():
    url = 'https://www.linkedin.com/pulse/steps-web-scraping-nlp-preparing-training-data-building-holi/'
    try:
        response = req.get(url)
        if response != 200:
            raise Exception("URL tidak valid")
    except Exception as valid:
        print(valid)
        return None
    return url

def scrape_page(url):
    respone = req.get(url)
    soup = bs(respone.text, "html.parser")
    # print(soup)
    content = soup.find('article').text
    # print(content)
    words = re.findall(r'\w+', content.lower())
    return words
def count_words(words):
    counter = collections.Counter(words)
    tagged_words = nltk.pos_tag(words)
    word_list = []
    for word, count in counter.items():
        tag = [tag for word, tag in tagged_words if word == word][0]
        word_list.append((word, tag, count))
    return word_list

def display_results(word_list):
    # Urutkan berdasarkan frekuensi
    word_list.sort(key=lambda x: x[2], reverse=True)
    # Ambil 10 kata dengan frekuensi terbesar
    word_list = word_list[:10]
    # print("{:<10} {:<10} {:<10}".format("Kata", "Tipe", "Frekuensi"))
    for word, tag, count in word_list:
        print("{:<10} {:<10} {:<10}".format(word, tag, count))
    word_counts = [count for word, tag, count in word_list]
    return word_counts

def main():
    url = check_url()
    words = scrape_page(url)
    word_list = count_words(words)
    display_results(word_list)

print(main())
    