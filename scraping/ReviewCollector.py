import scraping.ReviewScraper as ReviewScraper

class ReviewCollector:
    def __init__(self, scraper: ReviewScraper):
        self.scraper = scraper

    def collect_reviews(self, sources: dict) -> dict:
        all_reviews = {}
        for app_name, url in sources.items():
            reviews = self.scraper.scrape_reviews(url)
            if reviews:
                all_reviews[app_name] = reviews
        return all_reviews
