import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for saving to file
import matplotlib.pyplot as plt

output_dir = "data/graphs"

def load_reviews_with_drm_relevance(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_date(date_str):
    try:
        return pd.to_datetime(date_str, format='%m/%d/%Y')
    except ValueError:
        try:
            return pd.to_datetime(date_str, format='%d/%m/%Y')
        except ValueError:
            try:
                return pd.to_datetime(date_str, dayfirst=False)
            except ValueError:
                return pd.NaT

def plot_reviews_with_drm_relevance(filename: str):
    reviews = load_reviews_with_drm_relevance(filename)
    reviews_data = []

    for app, app_reviews in reviews.items():
        for review in app_reviews:
            if review.get('rating') is not None:  # Ensure rating is not None
                review['app'] = app  # Add the 'app' field to each review
                reviews_data.append(review)
    reviews_df = pd.DataFrame(reviews_data)
    reviews_df['date'] = reviews_df['date'].apply(parse_date)
    reviews_df = reviews_df[reviews_df['date'].dt.year >= 2015]
    reviews_df['normalized_rating'] = reviews_df['rating'] * 100
    
    plt.figure(figsize=(10, 6))
    total_points = 0
    plotted_points = 0

    for app, group in reviews_df.groupby('app'):
        total_points += len(group)
        valid_points = group.dropna(subset=['date', 'drm_relevance'])
        plotted_points += len(valid_points)
        avg_rating = group['rating'].mean()
        plt.scatter(valid_points['date'], valid_points['drm_relevance'], s=valid_points['normalized_rating'], label=f"{app} (Avg Rating: {avg_rating:.2f})", alpha=0.6)
        invalid_points = group[group.isna().any(axis=1)]
        if not invalid_points.empty:
            print(f"Unplotted points for {app}:")
            print(invalid_points[['date', 'drm_relevance']])
    
    plt.xlabel('Date')
    plt.ylabel('DRM Relavance Score')
    plt.title('Reviews DRM Relevance over Time with Normalized Product Ratings')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir + '/drm_relevance_with_ratings_over_time.png')

def plot_ratings_over_time(filename: str):
    reviews = load_reviews_with_drm_relevance(filename)
    reviews_data = []

    for app, app_reviews in reviews.items():
        for review in app_reviews:
            if review.get('rating') is not None:  # Ensure rating is not None
                review['app'] = app  # Add the 'app' field to each review
                reviews_data.append(review)
    reviews_df = pd.DataFrame(reviews_data)
    reviews_df['date'] = reviews_df['date'].apply(parse_date)
    reviews_df = reviews_df[reviews_df['date'].dt.year >= 2015]
    reviews_df['rating'] = reviews_df['rating'].astype(float)
    
    plt.figure(figsize=(10, 6))
    total_points = 0
    plotted_points = 0

    for app, group in reviews_df.groupby('app'):
        total_points += len(group)
        valid_points = group.dropna(subset=['date', 'rating'])
        plotted_points += len(valid_points)
        avg_rating = group['rating'].mean()
        plt.scatter(valid_points['date'], valid_points['rating'], label=f"{app} (Avg Rating: {avg_rating:.2f})", alpha=0.6)
        invalid_points = group[group.isna().any(axis=1)]
        if not invalid_points.empty:
            print(f"Unplotted points for {app}:")
            print(invalid_points[['date', 'rating']])
    
    plt.xlabel('Date')
    plt.ylabel('Rating')
    plt.title('Normalized Product Ratings over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir + '/ratings_over_time.png')

def plot_drm_relevance_vs_rating(filename: str):
    reviews = load_reviews_with_drm_relevance(filename)
    reviews_data = []

    for app, app_reviews in reviews.items():
        for review in app_reviews:
            if review.get('rating') is not None:  # Ensure rating is not None
                review['app'] = app  # Add the 'app' field to each review
                reviews_data.append(review)

    reviews_df = pd.DataFrame(reviews_data)
    
    # Ensure 'drm_relevance' and 'rating' are in the correct format and handle missing values
    reviews_df['drm_relevance'] = pd.to_numeric(reviews_df['drm_relevance'], errors='coerce')
    reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
    
    plt.figure(figsize=(10, 6))
    total_points = len(reviews_df)
    valid_points = reviews_df.dropna(subset=['drm_relevance', 'rating'])
    plotted_points = len(valid_points)
    
    for app, group in valid_points.groupby('app'):
        plt.scatter(group['drm_relevance'], group['rating'], label=app, alpha=0.6)
    
    if total_points != plotted_points:
        print(f"Error: {total_points - plotted_points} points could not be plotted due to missing or invalid data.")
        invalid_points = reviews_df[reviews_df.isna().any(axis=1)]
        print("Unplotted points:")
        print(invalid_points[['app', 'drm_relevance', 'rating']])
    
    plt.xlabel('DRM Relevance')
    plt.ylabel('Rating')
    plt.title('DRM Relevance vs Rating Analysis')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir + '/drm_relevance_vs_rating.png')

def plot_drm_relevance_by_rating_band(filename: str):
    reviews = load_reviews_with_drm_relevance(filename)
    reviews_data = []

    for app, app_reviews in reviews.items():
        for review in app_reviews:
            if review.get('rating') is not None:  # Ensure rating is not None
                review['app'] = app  # Add the 'app' field to each review
                reviews_data.append(review)
    reviews_df = pd.DataFrame(reviews_data)
    
    reviews_df['drm_relevance'] = pd.to_numeric(reviews_df['drm_relevance'], errors='coerce')
    reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
    reviews_df.dropna(subset=['drm_relevance', 'rating'], inplace=True)

    # Adjust the bins for normalized ratings
    rating_labels = ['Low (0-0.25)', 'Medium (0.25-0.5)', 'High (0.5-0.75)', 'Very High (0.75-1)']
    reviews_df['rating_band'] = pd.cut(reviews_df['rating'], bins=[0, 0.25, 0.5, 0.75, 1], labels=rating_labels, include_lowest=True)

    plt.figure(figsize=(12, 6))
    # Boxplot of DRM Relevance for each Rating Band
    reviews_df.boxplot(column='drm_relevance', by='rating_band', vert=False, grid=True, patch_artist=True)

    plt.title('DRM Relevance Distribution by Rating Band')
    plt.suptitle('')
    plt.xlabel('DRM Relevance Score')
    plt.ylabel('Rating Band')
    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_dir + '/drm_relevance_distribution_by_rating_band.png')

def calculate_drm_relevance_ratio(reviews_data: dict, relevance_threshold: float = 0.2, rating_threshold: float = 1.0) -> dict:
    product_ratios = {}
    for product, reviews in reviews_data.items():
        total_reviews = len(reviews)
        # Filter reviews based on rating threshold, handling None values explicitly
        low_rating_reviews = [review for review in reviews if review['rating'] is not None and float(review['rating']) < rating_threshold]
        relevant_reviews = sum(1 for review in low_rating_reviews if review['drm_relevance'] is not None and float(review['drm_relevance']) > relevance_threshold)
        # Calculate the ratio based on the count of low rating reviews
        ratio = relevant_reviews / total_reviews if total_reviews > 0 else 0
        product_ratios[product] = ratio
    return product_ratios

def plot_drm_relevance_ratio(filename):
    threshold = 0.2  # This is the relevance threshold for DRM
    reviews_data = load_reviews_with_drm_relevance(filename)
    product_ratios = calculate_drm_relevance_ratio(reviews_data, threshold, 1.0)

    # Sort products by ratio of reviews mentioning DRM
    sorted_products = sorted(product_ratios.items(), key=lambda x: x[1], reverse=True)

    # Prepare data for plotting
    products, ratios = zip(*sorted_products)

    plt.figure(figsize=(10, 6))
    bars = plt.barh(products, ratios, color='lightblue')
    plt.xlabel(f'Ratio of Reviews with DRM Relevance > {threshold}')
    plt.title(f'Ratio of Reviews with DRM Relevance > {threshold} by Product')
    plt.gca().invert_yaxis()

    # Annotate the bars with the ratio values
    for bar in bars:
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.2f}',
                 va='center', ha='right', color='blue', fontsize=8)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/drm_relevance_ratio_by_product.png')

def plot_negative_reviews_with_drm_relevance(filename: str):
    relevance_threshold = 0.2  # Threshold for considering a review relevant to DRM
    rating_threshold = 0.5  # Threshold for considering a review as negative

    reviews_data = load_reviews_with_drm_relevance(filename)
    product_ratios = calculate_drm_relevance_ratio(reviews_data, relevance_threshold, rating_threshold)

    # Sort products by ratio of negative reviews mentioning DRM
    sorted_products = sorted(product_ratios.items(), key=lambda x: x[1], reverse=True)

    # Prepare data for plotting
    products, ratios = zip(*sorted_products)

    plt.figure(figsize=(10, 6))
    bars = plt.barh(products, ratios, color='salmon')
    plt.xlabel(f'Ratio of Negative Reviews (Rating < {rating_threshold}) Mentioning DRM > {relevance_threshold}')
    plt.title(f'Ratio of Negative Reviews Mentioning DRM by Product')
    plt.gca().invert_yaxis()

    # Annotate the bars with the ratio values
    for bar in bars:
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.2f}',
                 va='center', ha='right', color='blue', fontsize=8)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/negative_reviews_with_drm_relevance.png')

def generate_plots(filename):
    plot_reviews_with_drm_relevance(filename)
    plot_ratings_over_time(filename)
    plot_drm_relevance_vs_rating(filename)
    plot_drm_relevance_by_rating_band(filename)
    plot_drm_relevance_ratio(filename)
    plot_negative_reviews_with_drm_relevance(filename)
