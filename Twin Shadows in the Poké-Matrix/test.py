import pandas as pd
from sklearn.linear_model import LinearRegression

# Final answer should be in flag format Hackemon{...}

# Load dataset
df = pd.read_csv("pokemon_training_dataset_200.csv")

# Prepare data
X = df[["HP", "Attack", "Defense", "SpAtk", "SpDef", "Speed"]]
y = df["Total"]

# Train model
model = LinearRegression()
model.fit(X, y)
preds = model.predict(X)
residuals = abs(y - preds)

# Find outliers
feature_outlier = df.loc[df["Attack"].idxmax(), "Name"]  # Meteorite
prediction_outlier = df.loc[residuals.idxmax(), "Name"]   # Hidden outlier

print(f"FLAG: {feature_outlier} {prediction_outlier}")

###  By the way, we love Hashing 111 ###