from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
from scraping.ReviewScraper import ReviewScraper

# Define the regions here, mapping your desired region codes to URL modifications if needed
REGIONS = {
    "us": "https://apps.apple.com/us/app/",
    "au": "https://apps.apple.com/au/app/",
    "ca": "https://apps.apple.com/ca/app/",
    "nz": "https://apps.apple.com/nz/app/",
}

class AppStoreReviewScraper(ReviewScraper):
    def parse_review(self, review_block, region: str):
        rating_label = review_block.find('figure', class_='we-star-rating').get('aria-label')
        rating_normalized = float(rating_label.split()[0]) / 5 if rating_label and 'out of' in rating_label else None
        
        user_element = review_block.find('span', class_='we-customer-review__user')
        user = user_element.text.strip() if user_element else 'Unknown'
        
        date_element = review_block.find('time', class_='we-customer-review__date')
        date = date_element.text.strip() if date_element else 'Unknown'
        
        title_element = review_block.find('h3', class_='we-truncate')
        title = title_element.text.strip() if title_element else 'No Title'
        
        body_element = review_block.find('blockquote', class_='we-truncate').p
        body = body_element.text.strip() if body_element else 'No Review Text'

        return {
            "rating": rating_normalized,
            "user": user,
            "date": date,
            "title": title,
            "body": body,
            "region": region
        }

    def scrape_reviews_for_region(self, base_url: str, region: str):
        # Construct the full URL based on the region
        url = f"{REGIONS[region]}{base_url}"
        print(f"Scraping {url}")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        
        response = requests.get(url, headers=headers)
        reviews = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'html.parser')
            review_blocks = soup.find_all('div', class_='we-customer-review lockup')

            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_review = {executor.submit(self.parse_review, review_block, region): review_block for review_block in review_blocks}
                
                for future in as_completed(future_to_review):
                    try:
                        review = future.result()
                        reviews.append(review)
                    except Exception as exc:
                        print(f"A review parsing generated an exception: {exc}")
        return reviews

    def scrape_reviews(self, base_url: str):
        all_reviews = []

        with ThreadPoolExecutor(max_workers=len(REGIONS)) as executor:
            future_to_region_reviews = {
                executor.submit(self.scrape_reviews_for_region, base_url, region): region
                for region in REGIONS
            }

            for future in as_completed(future_to_region_reviews):
                region = future_to_region_reviews[future]
                try:
                    region_reviews = future.result()
                    all_reviews.extend(region_reviews)
                except Exception as exc:
                    print(f"Region {region} generated an exception: {exc}")

        return all_reviews
