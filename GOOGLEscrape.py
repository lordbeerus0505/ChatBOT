'''
Scraping google to get results.
'''


import webbrowser
import requests
import mechanicalsoup

 
# to search

#from googlesearch.googlesearch import GoogleSearch

import requests
from bs4 import BeautifulSoup


USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}



def parse_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')

    found_results = []
    rank = 1
    result_block = soup.find_all('div', attrs={'class': 'g'})
    for result in result_block:

        link = result.find('a', href=True)
        title = result.find('h3', attrs={'class': 'r'})
        description = result.find('span', attrs={'class': 'st'})
        if link and title:
            link = link['href']
            title = title.get_text()
            if description:
                description = description.get_text()
            if link != '#':
                found_results.append({'keyword': keyword, 'rank': rank, 'title': title, 'description': description,'link':link})
                rank += 1
    return found_results
def fetch_results(search_term, number_results, language_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return search_term, response.text

class Search:
    def main(self,query,N):
        #query=input("Welcome, Enter your query")
        keyword, html = fetch_results(query, 10, 'en')
        #print(html)
        list=parse_results(html,keyword)
        if N==0:
            for l in list:
                if l['description']==None:
                    l['description']=' '
                print(l['title']+" "+str(l['description']+" "+str(l['link'])))
        if N==1:
            for l in list:
                if l['link'].find("youtube"):
                    webbrowser.open(l['link'])
                    return
        if N==2:
            for l in list:
                s=str(l['description'])
                #s="defn is to do something practical. Learn More. Pokemon is awesome."
                t=''
                #remove irrelevant text, go for the first sentence
                for i in s.split("."):
                    if "Learn More" not in i and "More example" not in i:
                        t=t+i
                print("\n"+t)
                break

            return

    #search(q)


