import requests
from bs4 import BeautifulSoup
import string


def scrap():
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"
    response = requests.get(url)

    if response:
        arr, new_arr, counter = [], [], 0

        soup = BeautifulSoup(response.content, 'html.parser')
        article = soup.find_all("article")
        soup_reborn = BeautifulSoup(str(article), 'html.parser')  # All articles
        span = soup_reborn.find_all("span", {"data-test": "article.type"})
        a = soup_reborn.find_all("a", {"data-track-action": "view article"})
        third_fucking_soup = BeautifulSoup(str(a), 'html.parser')

        for a in third_fucking_soup.find_all("a", href=True):
            new_arr.append(a["href"])

        for spa in span:
            if spa.text.strip() == "News":
                arr.append("https://www.nature.com" + new_arr[counter])  # Final Links
            counter += 1

        for file in arr:
            second_soup = BeautifulSoup(requests.get(file).content, 'html.parser')
            div = second_soup.find("div", {"class": "c-article-body"}).text.strip()
            title = second_soup.find("title").text

            for i in title:
                if i in string.punctuation:
                    title = title.replace(i, "")

            title = title.replace(" ", "_")
            file_name = open(title + ".txt", "wb")
            file_name.write(div.encode(encoding="UTF-8"))
            file_name.close()
            print("Article Saved")


scrap()
