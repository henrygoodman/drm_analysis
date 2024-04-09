from abc import ABC, abstractmethod

class ReviewScraper(ABC):
    @abstractmethod
    def scrape_reviews(self, url: str, region: str) -> list:
        pass