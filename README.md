# Engineering Capstone Research Project

## Project Overview

**Student**: Henry Goodman  
**ID**: 13032204  
**Institution**: University of Technology Sydney (UTS)

This project explores the impact of Digital Rights Management (DRM) on user experiences within various online media platforms. Utilizing Natural Language Processing (NLP), the study sifts through user reviews to extract sentiments pertaining to DRM and its implementations.

## Objective

The primary goal is to conduct a comparative analysis on the effects of DRM across popular online media products, with a focus on identifying the potential negative experiences users may encounter due to DRM practices.

## Methodology

- **Data Collection**: Accumulation of user reviews from app stores for selected media products.
- **NLP Analysis**: Application of NLP techniques to identify DRM-related keywords and sentiments within the collected reviews.
- **Visualization**: Generation of visual representations to showcase the relevance of DRM discussions and their correlation with user ratings over time.

## Tools and Technologies

- Programming Language: Python
- Libraries: pandas (for data manipulation), matplotlib (for data visualization)
- Custom modules for scraping and NLP analysis

## Usage

The project offers a command-line interface (CLI) for executing various functions. Ensure all dependencies are installed before running the commands:

```shell
pip install -r requirements.txt

# Generate reviews.json from specified URLs
python main.py --generate

# Analyze sentiments in the collected reviews
python main.py --analyze data/reviews.json

# Generate plots based on the analyzed data
python main.py --plot
```

## Results

Visualizations provide insight into DRM discussions within user reviews and their impact on product ratings:

### DRM Relevance Over Time with Product Ratings
![](/data/graphs/drm_relevance_with_ratings_over_time.png)

### DRM Relevance vs. Product Ratings
![](/data/graphs/drm_relevance_vs_rating.png)

### Product Ratings Over Time
![](/data/graphs/ratings_over_time.png)

## Conclusion

The findings suggest that DRM implementations can indeed influence user satisfaction. This underscores the necessity for a balanced DRM approach that safeguards content while maintaining a positive user experience.