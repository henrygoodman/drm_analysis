import toml
import pandas as pd

def load_drm_data(filename):
    with open(filename, 'r') as file:
        data = toml.load(file)
    return pd.json_normalize(data['products'])

def score_drm_features(data):
    # Define scores and weights
    feature_scores = {
        "none": 0, "low": 1, "moderate": 2, "high": 3, "very high": 4, "maximum": 5
    }

    weight_map = {
        'license_management': 1.5,
        'fair_use_facilitation': 1.5,
        'access_control_mechanisms': 1.5,
        'authentication_security': 1.2,
        'encryption_standards': 1.1,
    }

    # Apply scoring to DRM feature columns
    for column in data.columns:
        if column != 'name':  # Ignore the 'name' column for scoring
            data[column] = data[column].str.lower().map(feature_scores).fillna(0)
            if column in weight_map:
                data[column] *= weight_map[column]  # Apply weight if the column has a defined weight

    # Calculate the Total DRM Score by summing across the relevant columns
    data['Total DRM Score'] = data.iloc[:, 1:].sum(axis=1)
    
    return data

def main():
    filename = 'data/text/drm_data.toml'
    drm_data = load_drm_data(filename)
    scored_data = score_drm_features(drm_data)
    scored_data.to_csv('data/csv/drm_scores.csv', index=False)  # Save scores to CSV

if __name__ == "__main__":
    main()
