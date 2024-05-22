import requests
from bs4 import BeautifulSoup

url = 'https://example.com/page-to-scrape'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = soup.find_all('a')
    
    first_paragraph = soup.find('p').text
    
    print("Links:")
    for link in links:
        print(link['href'])
    
    print("\nFirst Paragraph:")
    print(first_paragraph)
else:
    print(f"Failed to retrieve the webpage (status code {response.status_code})")
