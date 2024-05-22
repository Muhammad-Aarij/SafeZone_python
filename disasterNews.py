from bs4 import BeautifulSoup
import requests

def scrape_news():
    url = "http://www.ndma.gov.pk/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_data = []

    # Using CSS selector to directly target the h4 tag for title within the nested structure
    articles = soup.select('article.post.clearfix.mb-30.bg-lighter')
    for article in articles:
        # Extract the title using the CSS path
        title_element = article.select_one('.entry-content .entry-meta .media-body .event-content h4.news.entry-title')
        entry_title = title_element.get_text(strip=True) if title_element else "N/A"

        # Extract the image source
        image_element = article.select_one('img.img-responsive.img-fullwidth.single_image')
        image_src = image_element['src'] if image_element else "N/A"

        # Extract the "Read more" link
        read_more_element = article.select_one('a.btn.btn-flat.read_more.btn-theme-colored.mt-5')
        read_more_link = read_more_element['href'] if read_more_element else "N/A"

        news_data.append({
            'entry_title': entry_title,
            'image_src': image_src,
            'read_more_link': read_more_link
        })

    return news_data

# Testing the function
if __name__ == "__main__":
    news_items = scrape_news()
    for item in news_items:
        print(item)
