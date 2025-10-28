import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin


class StarWarsWikiScraper:
    def __init__(self, base_url="https://starwars.fandom.com/wiki/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_page_content(self, page_name):
        url = urljoin(self.base_url, page_name)
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {page_name}: {e}")
            return None

    def extract_text(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        for element in soup.find_all(['script', 'style', 'nav', 'footer', 'aside']):
            element.decompose()

        content = soup.find('div', {'class': 'mw-parser-output'})
        if not content:
            return ""

        title = soup.find('h1', {'class': 'page-header__title'})
        title_text = title.get_text().strip() if title else "Unknown"

        paragraphs = []
        for element in content.children:
            if element.name == 'p':
                text = element.get_text().strip()
                if text and len(text) > 50:
                    paragraphs.append(text)

        return {
            'title': title_text,
            'content': '\n\n'.join(paragraphs[:10])
        }

    def save_document(self, data, filename):
        os.makedirs('knowledge_base/raw', exist_ok=True)
        filepath = f"knowledge_base/raw/{filename}.txt"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {data['title']}\n\n")
            f.write(data['content'])

        return filepath


PAGES_TO_DOWNLOAD = [
    "Luke_Skywalker", "Darth_Vader", "Leia_Organa", "Han_Solo", "Yoda",
    "Obi-Wan_Kenobi", "R2-D2", "C-3PO", "Chewbacca", "Emperor_Palpatine",
    "Boba_Fett", "Lando_Calrissian", "Stormtrooper", "Jabba_the_Hutt",
    "Millennium_Falcon", "Death_Star", "Lightsaber", "The_Force", "Jedi",
    "Sith", "Tatooine", "Hoth", "Endor", "Coruscant", "Naboo",
    "Clone_Wars", "Galactic_Empire", "Rebel_Alliance", "X-wing", "TIE_Fighter",
    "Blaster", "Speeder_Bike", "AT-AT", "Star_Destroyer"
]


def main():
    scraper = StarWarsWikiScraper()
    downloaded_pages = []

    for page in PAGES_TO_DOWNLOAD:
        print(f"Downloading {page}...")
        html_content = scraper.get_page_content(page)
        if html_content:
            text_data = scraper.extract_text(html_content)
            if text_data['content']:
                filename = scraper.save_document(text_data, page)
                downloaded_pages.append({
                    'original_name': page,
                    'file': filename,
                    'title': text_data['title']
                })
                print(f"✓ Saved {filename}")

        time.sleep(1)  # Уважаем сервер

    with open('knowledge_base/download_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(downloaded_pages, f, indent=2, ensure_ascii=False)

    print(f"\nDownloaded {len(downloaded_pages)} pages")


if __name__ == "__main__":
    main()