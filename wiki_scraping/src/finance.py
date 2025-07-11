import requests
from bs4 import BeautifulSoup
import threading
from lxml import html

yahoo_url = "https://finance.yahoo.com/quote/{symbol}"

class WikiWorker:
    def __init__(self):
        self._url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    @staticmethod
    def _extract_company_symbol(page_html):
        soup = BeautifulSoup(page_html, 'lxml')
        table = soup.find(id="constituents")
        table_rows = table.find_all('tr')
        for row in table_rows[1:]:
            symbol = row.find('td').text.strip("\n")
            yield symbol


    def _get_sp_500_symbols(self):
        response = requests.get(self._url)
        if response.status_code != 200:
            print("Couldn't fetch the S&P 500 companies list")
            return []

        yield from self._extract_company_symbol(response.text)
        

class YahooPriceWorker(threading.Thread):
    def __init__(self, symbol, **kwargs):
        super(YahooPriceWorker, self).__init__(**kwargs)
        self._symbol = symbol
        self._url = "https://finance.yahoo.com/quote/{self._symbol}"
        self.start() 

    def run(self):
        r = requests.get(self._url)
        page_contents = html.fromstring(r.text)
        price = page_contents.xpath("//*[@id='quote-header-info']/div[3]/div[1]/div/span[1]")
        print(price)

if __name__ == "__main__":
    wiki_worker = WikiWorker()
    current_workers = []
    for symbol in wiki_worker._get_sp_500_symbols():
        yahoo_price_worker = YahooPriceWorker(symbol = symbol)
        current_workers.append(yahoo_price_worker)

    for i in range(len(current_workers)):
        current_workers[i].join()

    
    