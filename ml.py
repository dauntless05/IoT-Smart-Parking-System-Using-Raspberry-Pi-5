import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

# Define days of the week
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Step 1: Load the dataset
df = pd.read_csv('parking_data_10_weeks.csv')  # Ensure your file is uploaded

# Step 2: Feature Engineering
# Convert 'Day' to categorical variable using one-hot encoding
df = pd.get_dummies(df, columns=["Day"], drop_first=True)

# Adding 'Weekday' feature (0 for weekday, 1 for weekend)
df['is_weekend'] = df['Week'].apply(lambda x: 1 if x in [6, 7] else 0)

# Create feature set 'X' and target variable 'y'
X = df.drop(['Cars_Parked'], axis=1)  # Features
y = df['Cars_Parked']  # Target variable

# Step 3: Train Test Split (Training on first 3 weeks, testing on the 4th week)
train_data = df[df['Week'] <= 3]  # Training data - first 3 weeks
test_data = df[df['Week'] == 4]  # Testing data - week 4

X_train = train_data.drop(['Cars_Parked'], axis=1)
y_train = train_data['Cars_Parked']
X_test = test_data.drop(['Cars_Parked'], axis=1)
y_test = test_data['Cars_Parked']

# Step 4: Train Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 5: Evaluate the model using Mean Absolute Error (MAE)
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")

# Step 6: Predict cars for next week (Week 5)
next_week_data = []

# Create features for the next week (assuming next week has the same structure)
for day in days_of_week:
    for hour in range(24):
        next_week_data.append([5, day, hour])  # Week 5, current day, current hour

# Convert to DataFrame
next_week_df = pd.DataFrame(next_week_data, columns=["Week", "Day", "Hour"])

# Feature Engineering for Next Week
next_week_df = pd.get_dummies(next_week_df, columns=["Day"], drop_first=True)
next_week_df['is_weekend'] = next_week_df['Week'].apply(lambda x: 1 if x in [6, 7] else 0)

# Predict parking demand for next week
predictions = model.predict(next_week_df)

# Add predictions to the DataFrame
next_week_df['Predicted_Cars_Parked'] = predictions

# Step 7: Save predictions to CSV
next_week_df.to_csv('predicted_parking_next_week.csv', index=False)

# To download the file
from google.colab import files
files.download('predicted_parking_next_week.csv')