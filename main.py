import argparse
import json
from scraping.AppStoreReviewScraper import AppStoreReviewScraper
from scraping.ReviewCollector import ReviewCollector
from nlp.nlp_sentiment_analysis import analyze_reviews_for_drm, load_reviews, save_reviews_with_score
from graphing.review_plotter import generate_plots

def save_reviews_to_json(reviews_dict: dict, filename: str):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(reviews_dict, f, ensure_ascii=False, indent=4)

def generate_reviews_json(urls: dict):
    all_reviews = {}
    app_store_scraper = AppStoreReviewScraper()
    collector = ReviewCollector(app_store_scraper)
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
        app_store_urls = {
            # E-books
            "Adobe Digital Editions": {
                "us": "https://apps.apple.com/us/app/adobe-digital-editions/id952977781?see-all=reviews",
                "ca": "https://apps.apple.com/ca/app/adobe-digital-editions/id952977781?see-all=reviews",
                "au": "https://apps.apple.com/au/app/adobe-digital-editions/id952977781?see-all=reviews",
                "nz": "https://apps.apple.com/nz/app/adobe-digital-editions/id952977781?see-all=reviews"
            },
            "Apple Books": {
                "us": "https://apps.apple.com/us/app/apple-books/id364709193?see-all=reviews",
                "ca": "https://apps.apple.com/ca/app/apple-books/id364709193?see-all=reviews",
                "au": "https://apps.apple.com/au/app/apple-books/id364709193?see-all=reviews",
                "nz": "https://apps.apple.com/nz/app/apple-books/id364709193?see-all=reviews",
            },
            # Audio Streaming
            "Audible": {
                "us": "https://apps.apple.com/us/app/audible-audiobooks-podcasts/id379693831?see-all=reviews",
                "ca": "https://apps.apple.com/ca/app/audible-audiobooks-podcasts/id379693831?see-all=reviews",
                "au": "https://apps.apple.com/au/app/audible-audiobooks-podcasts/id379693831?see-all=reviews",
                "nz": "https://apps.apple.com/nz/app/audible-audiobooks-podcasts/id379693831?see-all=reviews",
            },
            "Apple Music": {
                "us": "https://apps.apple.com/us/app/apple-music/id1108187390?see-all=reviews",
                "ca": "https://apps.apple.com/ca/app/apple-music/id1108187390?see-all=reviews",
                "au": "https://apps.apple.com/au/app/apple-music/id1108187390?see-all=reviews",
                "nz": "https://apps.apple.com/nz/app/apple-music/id1108187390?see-all=reviews",
            },
            # Video Streaming
            "Amazon Prime Video": {
                "us": "https://apps.apple.com/us/app/amazon-prime-video/id545519333?see-all=reviews",
                "ca": "https://apps.apple.com/ca/app/amazon-prime-video/id545519333?see-all=reviews",
                "au": "https://apps.apple.com/au/app/amazon-prime-video/id545519333?see-all=reviews",
                "nz": "https://apps.apple.com/nz/app/amazon-prime-video/id545519333?see-all=reviews",
            },
            "Netflix": {
                "us": "https://apps.apple.com/us/app/netflix/id363590051?see-all=reviews",
                "ca": "https://apps.apple.com/ca/app/netflix/id363590051?see-all=reviews",
                "au": "https://apps.apple.com/au/app/netflix/id363590051?see-all=reviews",
                "nz": "https://apps.apple.com/nz/app/netflix/id363590051?see-all=reviews",
            },
            # Gaming
            "Steam Mobile": {
                "us": "https://apps.apple.com/us/app/steam-mobile/id495369748?see-all=reviews",
                "ca": "https://apps.apple.com/ca/app/steam-mobile/id495369748?see-all=reviews",
                "au": "https://apps.apple.com/au/app/steam-mobile/id495369748?see-all=reviews",
                "nz": "https://apps.apple.com/nz/app/steam-mobile/id495369748?see-all=reviews",
            }
        }


        generate_reviews_json(app_store_urls)
    elif args.analyze:
        analyze_sentiment(args.analyze)
    elif args.plot:
        generate_plots("data/reviews_with_drm_relevance.json")
    else:
        parser.print_help()
