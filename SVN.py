import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Load the dataset
data_file = "02-16-2018.csv"  # Replace with your file path
data = pd.read_csv(data_file, low_memory=False)

# Inspect the dataset
print("Dataset structure before preprocessing:")
print(data.head())
print(data.info())

# Step 1: Encode categorical labels
label_encoder = LabelEncoder()
if 'Label' in data.columns:
    data['Label'] = label_encoder.fit_transform(data['Label'])
    print("Label Encoding Mapping:", dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))))

# Step 2: Handle missing or non-numeric values
# Replace non-numeric values with NaN and convert all columns to numeric
data = data.apply(pd.to_numeric, errors='coerce')

# Fill missing values with the mean for numeric columns
data = data.fillna(data.mean())

# Drop columns with more than 50% NaN values (if applicable)
data = data.loc[:, data.isnull().mean() < 0.5]

# Verify the structure after preprocessing
print("Dataset structure after preprocessing:")
print(data.info())

# Step 3: Split into features (X) and target (y)
X = data.drop(columns=['Label'], errors='ignore')  # Keep all columns except the target
y = data['Label']

# Check if X and y are valid
if X.empty or y.empty:
    print("Error: Features or labels are missing after preprocessing. Please check the dataset.")
    exit()

# Step 4: Normalize feature data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Step 5: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 6: SVM Model
svm_model = SVC(kernel='rbf', C=1, gamma='scale')  # Radial Basis Function kernel
svm_model.fit(X_train, y_train)

# Step 7: Evaluate the model
y_pred = svm_model.predict(X_test)

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nAccuracy Score:", accuracy_score(y_test, y_pred))
