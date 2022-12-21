from bs4 import BeautifulSoup
from flask import flash
import requests
import re


class Scrape:
    """
    Usage example:
    product1_scrape = Scrape(
        "https://beemybox.de/products/fahrradbox-basic-mit-zahlenschloss-solar-powerbank",
        "Ausverkauft")

    product1_scrape.get_html()
    product1_scrape.is_available()
    """

    def __init__(self, product_url, search_string):
        self.product_url = product_url
        self.search_string = search_string.lower()
        self.html = None

    def get_html(self):

        try:
            self.html = requests.get(self.product_url).text
            self.soup = BeautifulSoup(self.html, 'html.parser')
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            '''TODO: Flash incorrect URL'''
            print("URL is not available")

    def is_available(self):
        if self.html is not None:
            regex = r"<(\S*?)[ >]"
            matched_tags = self.soup.find_all(
                lambda tag: len(tag.find_all()) == 0 and self.search_string in tag.text.lower())

            accepted_tags = ["button", "p", "h1", "h2", "div"]

            for tag in matched_tags:
                regex_matches = re.match(regex, str(tag))
                regex_matches_parent = re.match(regex, str(tag.parent))
                if regex_matches.group(1) in accepted_tags or regex_matches_parent.group(1) in accepted_tags:
                    return False

            return True
        else:
            raise ValueError("Incorrect URL")
