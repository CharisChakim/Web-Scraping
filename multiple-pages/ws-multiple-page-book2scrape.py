import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd

start = int(input('Start Page to Scrape:' ))
end = int(input('Last Page to Scrape:' ))
books = []
for page in range(start,end+1):
    url = f'https://books.toscrape.com/catalogue/page-{page}.html'
    respone = req.get(url)
    # print(respone)
    respone = respone.content
    # print(respone)

    soup = bs(respone,'html.parser')

    order_list = soup.find('ol')
    articles = order_list.find_all('article', class_= 'product_pod')

    for article in articles:
        image = article.find('img')
        title = image.attrs['alt']
        star = article.find('p')
        star = star['class'][1]
        price = article.find('p', class_='price_color').text
        price = float(price[1:])
        books.append([title,price,star])
    # print(books)

df = pd.DataFrame(books,columns=['Title','Price','Star Rating'])
df.to_csv('results/result.csv')
print('Done')