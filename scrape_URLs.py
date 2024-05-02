import requests
from bs4 import BeautifulSoup
import os

def fetch_episode_urls(base_url, total_pages):
    episode_urls = []
    for page in range(1, total_pages + 1):
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            episodes = soup.find_all('h2', class_='programme__titles')
            for episode in episodes:
                link = episode.find('a', href=True)
                if link:
                    episode_urls.append(link['href'])
        else:
            print(f"Failed to fetch data from {url}")
    return episode_urls

def save_urls_to_file(urls, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        for url in urls:
            file.write(url + '\n')

if __name__ == "__main__":
    # URL of the episode list page (base URL)
    BASE_URL = "https://www.bbc.co.uk/programmes/b006qgvj/episodes/player"
    # Total number of pages, assuming 10 episodes per page and 758 episodes
    TOTAL_PAGES = (758 // 10) + (1 if 758 % 10 != 0 else 0)
    
    # Location to save the file - update before using
    FILE_PATH = r"path/to/episode_urls.txt"
    
    # Fetch the episode URLs
    urls = fetch_episode_urls(BASE_URL, TOTAL_PAGES)
    
    # Save the URLs to a file
    save_urls_to_file(urls, FILE_PATH)
    print("Episode URLs have been saved successfully.")
