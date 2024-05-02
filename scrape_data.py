import csv
import requests
from bs4 import BeautifulSoup

def extract_episode_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the date from the specified div element
        date_div = soup.find('div', class_="broadcast-event__time beta", attrs={"data-timezone": "true"})
        date_text = date_div['title'][0:11] if date_div and 'title' in date_div.attrs else "Date not found"
        
        # Find the short synopsis
        synopsis_div = soup.find('div', class_='synopsis-toggle__short')
        synopsis_text = synopsis_div.text.strip() if synopsis_div else "Synopsis not found"
        
        return (date_text, synopsis_text)
    else:
        return ("Failed to fetch data", "Failed to fetch data")

def read_urls_and_extract_info(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    
    with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['URL', 'Broadcast Date', 'Synopsis']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for url in urls:
            date_text, synopsis_text = extract_episode_info(url)
            writer.writerow({'URL': url, 'Broadcast Date': date_text, 'Synopsis': synopsis_text})
            print(f"Processed {url}")

# Inputs and outputs - update before use
if __name__ == "__main__":
    INPUT_FILE_PATH = r"path/to/episode_urls.txt"
    OUTPUT_FILE_PATH = r"path/to/episode_details.csv"
    
    read_urls_and_extract_info(INPUT_FILE_PATH, OUTPUT_FILE_PATH)
    print("Data extraction completed and saved to CSV.")
