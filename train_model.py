import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = 'https://medlineplus.gov'
index_url = f'{base_url}/healthtopics.html'

print("Fetching index page...")
response = requests.get(index_url)
soup = BeautifulSoup(response.content, 'html.parser')
print("Parsing index page...")

# Find all A-Z index page links
letter_links = soup.select('ul.alpha-links li a')
print(f"Found {len(letter_links)} letter index links.")

# Prepare CSV file
with open('medlineplus_health_topics.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Summary'])

    for letter_link in letter_links:
        letter_url = letter_link.get('href')

        # If the link doesn't start with 'http', prepend the base URL
        if not letter_url.startswith('http'):
            letter_url = base_url + letter_url
        
        print(f"Fetching letter page: {letter_url}")
        
        # Try to fetch the page with error handling
        try:
            letter_response = requests.get(letter_url)
            letter_response.raise_for_status()  # Raise an exception for HTTP errors
            letter_soup = BeautifulSoup(letter_response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {letter_url}: {e}")
            continue

        # Extract individual topic links from each letter page
        topic_links = letter_soup.select('ul.health-topics li a')

        for link in topic_links:
            topic_url = base_url + link.get('href')
            print(f"Fetching topic: {topic_url}")
            
            # Try to fetch the topic page with error handling
            try:
                topic_response = requests.get(topic_url)
                topic_response.raise_for_status()
                topic_soup = BeautifulSoup(topic_response.content, 'html.parser')
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {topic_url}: {e}")
                continue

            title = topic_soup.find('h1').get_text(strip=True)

            # Sometimes summary is inside the first paragraph or intro div
            summary_tag = topic_soup.find('div', class_='summary') or topic_soup.find('p')
            summary = summary_tag.get_text(strip=True) if summary_tag else ''

            # Write the data to the CSV
            writer.writerow([title, summary])
        
        # Add a delay to prevent overwhelming the server
        time.sleep(1)
