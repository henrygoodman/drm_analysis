import scraping.ReviewScraper as ReviewScraper

class ReviewCollector:
    def __init__(self, scraper: ReviewScraper):
        self.scraper = scraper

    def collect_reviews(self, sources: dict) -> dict:
        all_reviews = {}
        for app_name, region_urls in sources.items():
            all_reviews[app_name] = []
            for region, url in region_urls.items():
                reviews = self.scraper.scrape_reviews(url, region)
                if reviews:
                    all_reviews[app_name].extend(reviews)
        return all_reviews