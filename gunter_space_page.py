import requests
from yarl import URL
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import time

# Dokumentacja yarl/URL -> https://yarl.aio-libs.org/en/latest/api/
# Nawigowanie po drzewie -> https://www.crummy.com/software/BeautifulSoup/bs4/doc/#
# url elements -> https://blog.hubspot.com/marketing/parts-url

url_domain = "https://space.skyrocket.de"
url_subdirectory = "directories/chronology.htm"



def links_year(url_domain: str, url_subdirectory: str) -> list:
    url = str(URL(url_domain).with_path(url_subdirectory))

    response = requests.get(url, timeout=100, allow_redirects=False)

    if not response.ok:
        print(response.reason)

    soup = bs(response.text, 'html.parser')

    rows_year = soup.find_all('td')

    links_year = []
    for row in rows_year:
        year_link = row.find_all('a')
        links = [tag['href'] for tag in year_link]
        if links != []:
            links_year.append(links[0])
    return links_year


def flight_data(url_domain: str, list_link_years: str):

    for link in list_link_years[:1]:
        url = str(URL(url_domain).with_path(link)) # <- Tutaj trzeba iterować

        response = requests.get(url, timeout=100, allow_redirects=False)
        if not response.ok:
            print(response.reason)

        soup = bs(response.text, 'html.parser')

        launch_data = []
        mission_details_links = []

        table = soup.find('table', class_="data")

        headers = table.find_all('th')
        headers = [i.get_text() for i in table.find_all('th', class_=False)]

        rows = table.find_all('tr')
        for row in rows:
            data = [i.get_text() for i in row.find_all('td')]
            if data != []:
                launch_data.append(data)

            link_flight_details = row.find_all('a')
            link_flight_details = [tag['href'] for tag in link_flight_details]
            if link_flight_details != []:
                mission_details_links.append(link_flight_details[0]) # mission details -> link_flight_details[0], vehicle details -> link_flight_details[1]
                print(link_flight_details)
            time.sleep(1)

        launch_data = pd.DataFrame(launch_data, columns=headers)
    return launch_data, mission_details_links

def main():
    list_link_years = links_year(url_domain, url_subdirectory)

    # flights_data = flight_data(url_domain, list_link_years)[0]

    url = str(URL(url_domain).with_path('../doc_sdat/sputnik-1.htm'))
    response = requests.get(url, timeout=100, allow_redirects=False)
    if not response.ok:
        print(response.reason)

    soup = bs(response.text, 'html.parser')

    # # sat_description = soup.find('div', id='satdescription', class_=False).find_all('p')[1:] # <- to chyba nie jest najlepsze rozwiązanie [1:]
    sat_description = soup.find('div', id='satdescription', class_=False)
    sat_description = [i.get_text() for i in sat_description.find_all('p')]
    print(sat_description)
    sat_description = ''.join(str(x) for x in sat_description)

    print(sat_description)
    # Musisz jeszcze ściągnąć tabelkę z danymi lotu



if __name__ == '__main__':
    main()

