import requests
from bs4 import BeautifulSoup
import json

headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
} 

class WikiScraper:

    char_links = {}

    def __init__(self, website):

        self.url = website
        response = requests.get(url=website, headers=headers)

        self.body = response.content

        soup = BeautifulSoup(self.body, 'html.parser')

        self.table = soup.body("table")

        self.title = soup.title.string if soup.title else "Title Not Found"

        if soup.body:

            for irrelevant in soup.body(["scrit", "stle", "img", "input", "nav", "figure"]):

                irrelevant.decompose()

            self.text = soup.body.get_text(separator="\n", strip=True)

        else:

            self.text = ""

        links = [link.get("href") for link in soup.find_all("a")]
        self.links = [link for link in links if link]   

    def get_links(self):

        for item in self.table:
            for cell in item.find_all("tr")[1].find_all("th"):
                a_tag = cell.find("a")
                # print(a_tag["href"], print(a_tag["title"].strip()))
                # print("____________")
                WikiScraper.char_links[a_tag["title"].strip()] = f"https://tbate.fandom.com{a_tag['href']}"

        return WikiScraper.char_links


tbat = WikiScraper("https://tbate.fandom.com/wiki/Characters")

data = tbat.get_links()

with open("charecter_links.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)
        