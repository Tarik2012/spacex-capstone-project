import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

def load_and_preprocess(test_size=0.2, random_state=42):
    # 1. Build absolute path to dataset
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_path = os.path.join(base_dir, "data", "processed", "clean_dataset.csv")

    # 2. Load dataset
    df = pd.read_csv(data_path)

    # 3. Imputations
    df["payload"] = df["payload"].fillna(df["payload"].median())
    df["flight"] = df["flight"].fillna(df["flight"].median()).astype(int)
    df[["gridfins", "reused", "legs"]] = (
        df[["gridfins", "reused", "legs"]].fillna(False).astype(bool)
    )
    df["orbit"] = df["orbit"].fillna("Unknown").replace("", "Unknown")
    df["site"]  = df["site"].fillna("Unknown").replace("", "Unknown")

    # 4. Define features & target
    X = df[["flight", "payload", "orbit", "site", "gridfins", "reused", "legs"]]
    y = df["success"]   # 👈 asegúrate que tu target se llama "success"

    # 5. Preprocessor
    numeric_features = ["flight", "payload"]
    categorical_features = ["orbit", "site"]
    boolean_features = ["gridfins", "reused", "legs"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(sparse_output=False, handle_unknown="ignore"), categorical_features),
            ("bool", "passthrough", boolean_features),
        ]
    )

    # 6. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    return X_train, X_test, y_train, y_test, preprocessor
