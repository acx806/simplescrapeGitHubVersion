from bs4 import BeautifulSoup
import requests


class Scrape():

    def __init__(self, product_url, search_string):
        self.product_url = product_url
        self.search_string = search_string

    def get_html(self):
        self.html = requests.get(self.product_url).text
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def is_available(self):

        matched_tags = self.soup.find_all(lambda tag: len(tag.find_all()) == 0 and self.search_string in tag.text)

        for tag in matched_tags:
            print(tag.unwrap())
            #temp_soup = BeautifulSoup(tag,'html.parser')
            #print("HEY NEW TAG!!!"+temp_soup.prettify()+"\n\n\n\n\n\n\n")


product1_scrape = Scrape(
    "https://beemybox.de/products/fahrradbox-basic-mit-zahlenschloss-solar-powerbank",
    "Ausverkauft")

product1_scrape.get_html()
product1_scrape.is_available()
