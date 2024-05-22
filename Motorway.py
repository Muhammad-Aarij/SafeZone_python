import requests
from bs4 import BeautifulSoup

def scrape_motorway_data():
    url = "https://nwfc.pmd.gov.pk/new/fog-motorways.php"
    # Set the user agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Send an HTTP GET request to the webpage with the specified headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize a dictionary to store the scraped data
        scraped_data = {}

        # Loop through each div with id starting from tab1 to tab7
        for i in range(1, 8):
            div_id = f"tab{i}"

            # Find the div with the specified id
            tab_div = soup.find('div', id=div_id)

            if tab_div:
                print(f"Tab div {div_id} found!")

                # Find the table inside the div
                table = tab_div.find('table')

                if table:
                    # Find all the th elements in the thead
                    headers = [th.text.strip() for th in table.find('thead').find_all('th')]

                    # Find all the tr elements in the tbody
                    rows = table.find('tbody').find_all('tr')

                    # Initialize a list to store the data for the current div
                    div_data = []

                    # Loop through each row in the tbody
                    for row in rows:
                        # Find all the td elements in the row
                        cells = row.find_all('td')

                        # Create a dictionary with the scraped data
                        entry = {}
                        for j in range(len(headers)):
                            key = headers[j]
                            value = cells[j].text.strip()

                            # If the value is inside a <span> tag with class "label-success", extract the text from it
                            span_tag = cells[j].find('span', class_='label-success')
                            if span_tag:
                                value = span_tag.text.strip()

                            entry[key] = value

                        # Append the dictionary to the list
                        div_data.append(entry)

                    # Add the data for the current div to the dictionary
                    scraped_data[div_id] = div_data

        return scraped_data
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

# Example usage
result = scrape_motorway_data()

if result:
    # Print the scraped data
    for div_id, data in result.items():
        print(f"\nData for {div_id}:")
        for entry in data:
            print(entry)
