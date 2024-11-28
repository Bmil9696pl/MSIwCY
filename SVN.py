import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Wczytaj zbiór danych
data_file = "cleaned_data.csv"  # Podaj ścieżkę do pliku
data = pd.read_csv(data_file, low_memory=False)

# Wyświetl strukturę zbioru danych
print("Struktura zbioru danych przed przetwarzaniem:")
print(data.head())
print(data.info())

# Krok 1: Zakoduj etykiety kategoryczne
label_encoder = LabelEncoder()
if 'Label' in data.columns:
    data['Label'] = label_encoder.fit_transform(data['Label'])
    print("Mapowanie kodowania etykiet:", dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))))

# Krok 2: Obsłuż brakujące lub nienumeryczne wartości
# Zamień nienumeryczne wartości na NaN i skonwertuj wszystkie kolumny na wartości numeryczne
data = data.apply(pd.to_numeric, errors='coerce')

# Usuń kolumny z więcej niż 50% brakującymi wartościami (jeśli takie istnieją)
data = data.loc[:, data.isnull().mean() < 0.5]

# Uzupełnij brakujące wartości średnią w kolumnach numerycznych
data = data.fillna(data.mean())

# Zweryfikuj strukturę po przetwarzaniu
print("Struktura zbioru danych po przetwarzaniu:")
print(data.info())

# Krok 3: Podział na cechy (X) i etykiety (y)
X = data.drop(columns=['Label'], errors='ignore')  # Zachowaj wszystkie kolumny poza etykietą
y = data['Label']

# Sprawdź, czy X i y są poprawne
if X.empty or y.empty:
    print("Błąd: Cechy lub etykiety są puste po przetwarzaniu. Sprawdź zbiór danych.")
    exit()

# Krok 4: Normalizacja danych wejściowych
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Krok 5: Podział na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Krok 6: Model SVM
svm_model = SVC(kernel='rbf', C=1, gamma='scale')  # Jądro RBF (Radial Basis Function)
svm_model.fit(X_train, y_train)

# Krok 7: Ocena modelu
y_pred = svm_model.predict(X_test)

print("Macierz konfuzji:")
print(confusion_matrix(y_test, y_pred))

print("\nRaport klasyfikacji:")
print(classification_report(y_test, y_pred))

print("\nDokładność (Accuracy):", accuracy_score(y_test, y_pred))
