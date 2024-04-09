import requests
from bs4 import BeautifulSoup
from scraping.ReviewScraper import ReviewScraper

class AppStoreReviewScraper(ReviewScraper):
    def scrape_reviews(self, url: str, region: str) -> list:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'html.parser')
            review_blocks = soup.find_all('div', class_='we-customer-review lockup')

            reviews = []
            for review_block in review_blocks:
                rating_label = review_block.find('figure', class_='we-star-rating').get('aria-label')
                
                # Normalize the rating to a fraction
                rating_parts = rating_label.split(' out of ')
                if len(rating_parts) == 2:
                    rating_value, max_rating = rating_parts[0], rating_parts[1].split()[0]  # Extracts "X" from "X stars"
                    rating_normalized = float(rating_value) / float(max_rating)  # Convert to fraction
                else:
                    rating_normalized = None  # In case the format is unexpected
                
                user = review_block.find('span', class_='we-customer-review__user').text.strip()
                date = review_block.find('time', class_='we-customer-review__date').text.strip()
                title = review_block.find('h3', class_='we-truncate').text.strip()
                body = review_block.find('blockquote', class_='we-truncate').p.text.strip()

                review = {
                    "rating": rating_normalized,
                    "user": user,
                    "date": date,
                    "title": title,
                    "body": body,
                    "region": region
                }
                reviews.append(review)

            return reviews
        else:
            print("Failed to fetch reviews for", url)
            return []
