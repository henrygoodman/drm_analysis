import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(drm_file, reviews_file):
    drm_scores = pd.read_csv(drm_file)
    review_ratios = pd.read_csv(reviews_file)
    drm_scores.rename(columns={'name': 'Product'}, inplace=True)
    return drm_scores, review_ratios

def merge_and_correlate(drm_scores, review_ratios, method='spearman'):
    merged_data = pd.merge(drm_scores, review_ratios, on='Product')
    filtered_data = merged_data[['Total DRM Score', 'Negative DRM Relevance Ratio', 'Product']]
    numeric_data = filtered_data.select_dtypes(include=[np.number])
    correlation = numeric_data.corr(method=method)  
    return correlation, filtered_data

def plot_data(filtered_data, method='spearman'):
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='Total DRM Score', y='Negative DRM Relevance Ratio', hue='Product', data=filtered_data, palette='deep', s=100)
    sns.regplot(x='Total DRM Score', y='Negative DRM Relevance Ratio', data=filtered_data, scatter=False, color='black')
    
    if method == 'spearman':
        corr_coef = filtered_data['Total DRM Score'].corr(filtered_data['Negative DRM Relevance Ratio'], method='spearman')
    else:
        corr_coef = filtered_data['Total DRM Score'].corr(filtered_data['Negative DRM Relevance Ratio'], method='pearson')
    
    plt.title(f'Scatter Plot of DRM Score vs. Negative Review Ratio\n{method.capitalize()} correlation coefficient: {corr_coef:.2f}')
    plt.xlabel('Total DRM Score')
    plt.ylabel('Negative DRM Relevance Ratio')
    plt.grid(True)
    plt.legend(title='Product', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f'data/graphs/scatter_plot_correlation_{method}.png')

def main():
    drm_scores, review_ratios = load_data('data/csv/drm_scores.csv', 'data/csv/negative_reviews_with_drm_relevance.csv')
    print("Checking Spearman Correlation:")
    spearman_results, spearman_data = merge_and_correlate(drm_scores, review_ratios, 'spearman')
    print("Spearman Correlation Matrix:\n", spearman_results)
    plot_data(spearman_data, 'spearman')

    print("Checking Pearson Correlation:")
    pearson_results, pearson_data = merge_and_correlate(drm_scores, review_ratios, 'pearson')
    print("Pearson Correlation Matrix:\n", pearson_results)
    plot_data(pearson_data, 'pearson')

if __name__ == "__main__":
    main()
