import re
import collections
import nltk
from urllib.request import urlopen
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Fungsi untuk mengambil URL dari user dan melakukan validasi
def get_url():
    url = input("Masukkan URL: ")
    try:
        response = urlopen(url)
        if response.getcode() != 200:
            raise Exception("URL tidak valid")
    except Exception as e:
        print(e)
        return None
    return url

# Fungsi untuk melakukan scraping dan parsing halaman web
def scrape_page(url):
    response = urlopen(url)
    soup = BeautifulSoup(response, "html.parser")
    content = soup.get_text()
    words = re.findall(r'\w+', content.lower())
    return words

# Fungsi untuk menghitung frekuensi setiap kata dan menentukan tipe kata
def count_words(words):
    counter = collections.Counter(words)
    tagged_words = nltk.pos_tag(words)
    word_list = []
    for word, count in counter.items():
        tag = [tag for word, tag in tagged_words if word == word][0]
        word_list.append((word, tag, count))
    return word_list

# Fungsi untuk menampilkan tabel dan grafik frekuensi kata
def display_results(word_list):
    # Urutkan berdasarkan frekuensi
    word_list.sort(key=lambda x: x[2], reverse=True)
    # Ambil 10 kata dengan frekuensi terbesar
    word_list = word_list[:10]
    # print("{:<10} {:<10} {:<10}".format("Kata", "Tipe", "Frekuensi"))
    for word, tag, count in word_list:
        print("{:<10} {:<10} {:<10}".format(word, tag, count))
    word_counts = [count for word, tag, count in word_list]
    plt.bar(range(len(word_list)), word_counts)
    plt.xticks(range(len(word_list)), [word for word, tag, count in word_list], rotation=90)
    plt.show()
    

# Fungsi utama
def main():
    url = get_url()
    if url is None:
        return
    # nltk.download(averaged_perceptron_tagger)
    words = scrape_page(url)
    word_list = count_words(words)
    display_results(word_list)

if __name__ == "__main__":
    main()
