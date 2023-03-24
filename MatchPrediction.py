import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer


# Load the data into a pandas dataframe
df = pd.read_csv('/content/speeddating.csv')

def decode_and_strip(x):
    return str(x).replace("b'", "").replace("'", "").strip()

df = df.drop(['sports', 'tvsports', 'exercise', 'dining', 'museums', 'art', 'hiking', 'gaming', 'clubbing', 'reading', 'tv', 'theater', 'movies', 'concerts', 'music', 'shopping', 'yoga', 'd_sports', 'd_tvsports', 'd_exercise', 'd_dining', 'd_museums', 'd_art', 'd_hiking', 'd_gaming', 'd_clubbing', 'd_reading', 'd_tv', 'd_theater', 'd_movies', 'd_concerts', 'd_music', 'd_shopping', 'd_yoga', 'field', 'wave'], axis=1)


# Apply the function to all elements in the DataFrame
df = df.applymap(decode_and_strip)

def replace_median(df):
    for col in df.columns:
        if df[col].dtype == 'O' and '-' in str(df[col].iloc[0]):
            bounds = df[col].str.extract(r'\[(\d+)-(\d+)\]')
            bounds = bounds.apply(pd.to_numeric)
            medians = bounds.mean(axis=1)
            df[col] = medians
    return df

# Replace some columns with the median of their values
df = replace_median(df)

# Fill the NaN values with the median of their respective columns
df = df.fillna(method='ffill').fillna(method='bfill')

# One-hot encode categorical variables
cat_cols = ["has_null", "gender", "race", "race_o"]
X_cat = pd.get_dummies(df[cat_cols], prefix=cat_cols, columns=cat_cols)

# Scale the numerical variables
num_cols = [col for col in df.columns if col not in cat_cols and col != "match"]
scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

# Combine the numerical and categorical features
X = pd.concat([df[num_cols], X_cat], axis=1)

# Drop unwanted columns
X = X.drop(["guess_prob_liked", "like", "d_like", "d_guess_prob_liked", "met", "decision", "decision_o"], axis=1)

y = df["match"].astype(int)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Replace missing values with the mean of the respective columns
imputer = SimpleImputer(strategy='mean')
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)

# Fit the Random Forest Model ( highest performance out of attempted model architectures)
clf = RandomForestClassifier(n_estimators=100, criterion = "gini", max_depth = 30, random_state=42)
clf.fit(X_train, y_train)

# Make predictions on the test data
y_pred = clf.predict(X_test)

# Calculate the accuracy of the classifier
accuracy = accuracy_score(y_test, y_pred)

# Print the accuracy of the classifier
print("Accuracy:", accuracy)

import matplotlib.pyplot as plt

# Get feature importances
importances = clf.feature_importances_

# Get header row of the dataframe
header = list(X.columns)

# Sort feature importances in descending order
sorted_idx = importances.argsort()[::-1]
# Create bar chart of feature importances
plt.figure(figsize=(70, 35))
plt.bar(range(len(sorted_idx)), importances[sorted_idx], align='center')
plt.xticks(range(len(sorted_idx)), [header[i] for i in sorted_idx], rotation=90, fontsize=16)
plt.title("Feature Importances", fontsize=30)
plt.xlabel("Features", fontsize=28)
plt.ylabel("Importance", fontsize=28)
plt.show()
