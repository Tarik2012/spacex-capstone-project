import sys, os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline

# ✅ Ensure Python can find the scripts/ folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.preprocessing import load_and_preprocess

# --- Step 1: Load data ---
X_train, X_test, y_train, y_test, preprocessor = load_and_preprocess()

# --- Step 2: Define the final model (best hyperparameters) ---
rf_final = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=2,
    class_weight="balanced",
    random_state=42
)

# --- Step 3: Build pipeline (preprocessor + model) ---
final_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", rf_final)
])

# --- Step 4: Train model ---
final_pipeline.fit(X_train, y_train)

# --- Step 5: Evaluate quickly on test ---
y_pred = final_pipeline.predict(X_test)
print("📊 Classification Report (Final RF):")
print(classification_report(y_test, y_pred))

# --- Step 6: Save model ---
os.makedirs("models", exist_ok=True)
model_path = os.path.join("models", "random_forest_model.joblib")
joblib.dump(final_pipeline, model_path)
print(f"✅ Model saved at {model_path}")
