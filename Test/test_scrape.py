import pytest
from Frontend import Scrape

'''
Initialize scrape objects
'''
sold_out = Scrape.Scrape("https://www.socklaender.de/products/funktions-socke-2er-set", "ausverkauft")
sold_out.get_html()

available = Scrape.Scrape("https://www.schreibathlet.de/collections/alle-hefte/products/schreibschrift-heft", "ausverkauft")
available.get_html()

incorrect = Scrape.Scrape("https://beemyox.de/products/powerbank-solardeckel", "ausverkauft")
incorrect.get_html()
'''
Tests
'''
def test_scrape_sold_out():
    assert sold_out.is_available() is False


def test_scrape_available():
    assert available.is_available()


def test_incorrect_url():
    with pytest.raises(ValueError):
        incorrect.is_available()