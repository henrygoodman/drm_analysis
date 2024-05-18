# Engineering Capstone Research Project

## Project Overview

**Student**: Henry Goodman  
**ID**: 13032204  
**Institution**: University of Technology Sydney (UTS)

This project explores the impact of Digital Rights Management (DRM) on user experiences within various online media platforms. Utilizing Natural Language Processing (NLP), the study sifts through user reviews to extract sentiments pertaining to DRM and its implementations.

## Objective

The primary goal is to conduct a comparative analysis on the effects of DRM across popular online media products, with a focus on identifying the potential negative experiences users may encounter due to DRM practices.

## Methodology

### Data Collection
Data was strategically gathered from multiple digital platforms known for implementing DRM, including e-books, audio streaming services, video streaming platforms, and gaming applications. A custom-built web scraper was developed to automate the extraction of essential information such as the review date, user's rating, and the full text of each review, ensuring a broad and representative dataset.

### NLP Analysis
The collected data underwent preprocessing, including tokenization, normalization, and lemmatization, to facilitate detailed sentiment analysis focused on DRM-related aspects. An extensive set of DRM-related keywords was identified to pinpoint relevant sentiments in the reviews.

### Visualization
Advanced data visualization techniques were employed to generate graphical representations of the data, highlighting the prevalence of DRM discussions and their correlation with user ratings over time.

## Tools and Technologies

- **Programming Language**: Python
- **Libraries**: 
  - pandas: Used for data manipulation and analysis.
  - matplotlib and seaborn: Employed for generating static, interactive, and animated visualizations.
  - Natural Language Toolkit (NLTK): Applied for comprehensive NLP tasks.
- **Custom Modules**: Developed for specific tasks like web scraping, data cleaning, and sentiment analysis.

## Usage

The project offers a command-line interface (CLI) for executing various functions. Ensure all dependencies are installed before running the commands:

```zsh
# Install project requirements
pip install -r requirements.txt

# Generate reviews.json from specified URLs
python main.py --generate

# Analyze sentiments in the collected reviews
python main.py --analyze

# Generate plots based on the analyzed data
python main.py --plot

# Generate rankings .csv file from DRM Complexity toml file
python main.py --rank

# Generate correlation analyses from generated .csv files
python main.py --gencor
```

## Results

Visualizations provide insight into DRM discussions within user reviews and their impact on product ratings:

### DRM Relevance Over Time with Product Ratings
![](/data/graphs/drm_relevance_with_ratings_over_time.png)

### Rankings Ratio of DRM Relavant Reviews to Total Reviews
![](/data/graphs/drm_relevance_ratio_by_product.png)

### Rankings Ratio of DRM Relavant Reviews to Total Reviews (excluding positive reviews)
![](/data/graphs/negative_reviews_with_drm_relevance.png)

### DRM Relevance vs. Product Ratings
![](/data/graphs/drm_relevance_vs_rating.png)

### DRM Relevance vs. Product Ratings, excluding DRM Relevance = 0 (Boxplot distribution)
![](/data/graphs/drm_relevance_distribution_by_rating_band_excluding_non_mentioned.png)

### Product Ratings Over Time
![](/data/graphs/ratings_over_time.png)

### Pearson Correlation (DRM Complexity Scores vs Negative Review ratio)
![](/data/graphs/scatter_plot_correlation_pearson.png)

### Spearman Correlation (DRM Complexity Scores vs Negative Review ratio)
![](/data/graphs/scatter_plot_correlation_spearman.png)
