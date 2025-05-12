# train_model.py
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load and preprocess dataset
df = pd.read_csv('dataset.csv')

# CSV de bozuk datalar varsa (Nan) onları temizleyelim.
df = df.dropna()

# Convert categorical columns to numeric
df_encoded = pd.get_dummies(df.drop(columns=['ID', 'Var_1']))
X = df_encoded
y = df['Var_1']

# Train model
model = DecisionTreeClassifier()

print(X.head())
print(X.dtypes)
print("X shape:", X.shape)
print("y shape:", y.shape)
print("Null values in X:", X.isnull().sum().sum())
print("Null values in y:", y.isnull().sum())


model.fit(X, y)

# Save model
joblib.dump((model, list(X.columns)), 'decision_tree_model.pkl')
