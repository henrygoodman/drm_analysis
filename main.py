import argparse
import json
from scraping.AppStoreReviewScraper import AppStoreReviewScraper
from scraping.TrustPilotReviewScraper import TrustPilotReviewScraper
from scraping.ReviewCollector import ReviewCollector
from nlp.nlp_sentiment_analysis import analyze_reviews_for_drm, load_reviews, save_reviews_with_score
from graphing.review_plotter import generate_plots

def save_reviews_to_json(reviews_dict: dict, filename: str):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(reviews_dict, f, ensure_ascii=False, indent=4)

def generate_reviews_json(scraper_urls_pairs: list):
    all_reviews = {}
    for scraper, urls in scraper_urls_pairs:
        collector = ReviewCollector(scraper)
        all_reviews.update(collector.collect_reviews(urls))
    save_reviews_to_json(all_reviews, "data/reviews.json")

def analyze_sentiment(filename: str):
    reviews = load_reviews(filename)
    analyzed_reviews = analyze_reviews_for_drm(reviews)
    save_reviews_with_score(analyzed_reviews, "data/reviews_with_drm_relevance.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="App review scraper and sentiment analysis tool")
    parser.add_argument("--generate", action="store_true", help="Generate reviews.json")
    parser.add_argument("--analyze", action="store", metavar="FILENAME", help="Run sentiment analysis on existing reviews.json")
    parser.add_argument("--plot", action="store_true", help="Plot reviews with DRM score")
    args = parser.parse_args()

    if args.generate:
        app_store_scraper = AppStoreReviewScraper()
        trustpilot_scraper = TrustPilotReviewScraper()

        app_store_urls = {
            "Adobe Digital Editions": "adobe-digital-editions/id952977781?see-all=reviews",
            "Apple Books": "apple-books/id364709193?see-all=reviews",
            "Audible": "audible-audiobooks-podcasts/id379693831?see-all=reviews",
            "Apple Music": "apple-music/id1108187390?see-all=reviews",
            "Amazon Prime Video": "amazon-prime-video/id545519333?see-all=reviews",
            "Netflix": "netflix/id363590051?see-all=reviews",
            "Steam Mobile": "steam-mobile/id495369748?see-all=reviews",
        }

        trustpilot_urls = {
            "eBooks": "dl.ebooks.com",
            "Steam": "www.steampowered.com",
            "Ubisoft": "www.ubisoft.com",
            "Electronic Arts (EA)": "www.ea.com",
        }

        scraper_urls_pairs = [
            (app_store_scraper, app_store_urls),
            (trustpilot_scraper, trustpilot_urls),
        ]

        generate_reviews_json(scraper_urls_pairs)

    elif args.analyze:
        analyze_sentiment(args.analyze)
    elif args.plot:
        generate_plots("data/reviews_with_drm_relevance.json")
    else:
        parser.print_help()
