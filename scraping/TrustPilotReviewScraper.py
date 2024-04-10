from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
from scraping.ReviewScraper import ReviewScraper
from datetime import datetime

NUM_PAGES = 80

# TrustPilot shows the same reviews no matter the region
REGIONS = {
    "us": "www",
}

class TrustPilotReviewScraper(ReviewScraper):
    def fetch_page(self, url: str):
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        return response.content if response.status_code == 200 else None

    def parse_reviews(self, content, region: str):
        reviews = []
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            review_blocks = soup.find_all('article', class_='styles_reviewCard__hcAvl')

            for review_block in review_blocks:
                rating_element = review_block.find('img', alt=True)
                rating_text = rating_element['alt'] if rating_element else None
                rating_normalized = float(rating_text.split()[1]) / 5 if rating_text and 'out of' in rating_text else None

                user_element = review_block.find('span', class_='typography_heading-xxs__QKBS8')
                user = user_element.text.strip() if user_element else 'Unknown'

                date_element = review_block.find('time')
                date_str = date_element['datetime'] if date_element else 'Unknown'
                date = 'Unknown'
                if date_str != 'Unknown':
                    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                    date = date_obj.strftime("%Y-%m-%d")

                title_element = review_block.find('h2', class_='typography_heading-s__f7029')
                title = title_element.text.strip() if title_element else 'No Title'

                body_element = review_block.find('div', class_='styles_reviewContent__0Q2Tg')
                body = body_element.p.text.strip() if body_element and body_element.p else 'No Review Text'

                reviews.append({
                    "rating": rating_normalized,
                    "user": user,
                    "date": date,
                    "title": title,
                    "body": body,
                    "region": region
                })
        return reviews

    def scrape_region(self, base_url: str, region_code: str):
        all_reviews = []
        region_url = f"https://{REGIONS[region_code]}.trustpilot.com/review/{base_url}"
        print(f"Scraping {region_url}")

        with ThreadPoolExecutor(max_workers=NUM_PAGES) as page_executor:
            future_to_page = {
                page_executor.submit(self.fetch_page, f"{region_url}?page={page}"): page
                for page in range(1, NUM_PAGES + 1)
            }

            for future in as_completed(future_to_page):
                content = future.result()
                page_reviews = self.parse_reviews(content, region_code)
                all_reviews.extend(page_reviews)

        return all_reviews

    def scrape_reviews(self, base_url: str):
        all_reviews = []

        with ThreadPoolExecutor(max_workers=len(REGIONS)) as executor:
            future_to_region_reviews = {executor.submit(self.scrape_region, base_url, region): region for region in REGIONS}

            for future in as_completed(future_to_region_reviews):
                try:
                    region_reviews = future.result()
                    all_reviews.extend(region_reviews)  # Flattening the list of reviews
                except Exception as exc:
                    print(f"An exception occurred: {exc}")

        return all_reviews
