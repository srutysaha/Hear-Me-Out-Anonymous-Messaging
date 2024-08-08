import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset from the CSV file
df = pd.read_csv('category.csv')

# Preprocessing and Feature Extraction
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['message'])
y = df['category']

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training the model
model = MultinomialNB()
model.fit(X_train, y_train)

# Predicting and Evaluating
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
# print("Classification Report:\n", classification_report(y_test, y_pred))
# # Transforming the new complaints to the same feature space as the training data
def category_predict(a):
    new_complaints_transformed = vectorizer.transform(a)
    predictions = model.predict(new_complaints_transformed)
    print(predictions[0])
    return predictions[0]

# new_complaints = [
#     "The canteen food quality has decreased",
#     "Seniors are harassing new students",
#     "The library lacks sufficient study materials"
# ]


# Making predictions
