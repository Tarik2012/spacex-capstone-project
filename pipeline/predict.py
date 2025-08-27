import sys, os
import joblib
import pandas as pd

# ✅ Ensure Python can find scripts/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --- Step 1: Load saved model ---
model_path = os.path.join("models", "random_forest_model.joblib")
model = joblib.load(model_path)
print(f"✅ Loaded model from {model_path}")

# --- Step 2: Example batch of new data ---
new_data = pd.DataFrame([
    {"flight": 130, "payload": 5500, "orbit": "LEO", "site": "KSC LC-39A", "gridfins": True,  "reused": True,  "legs": True},
    {"flight": 5,   "payload": 8000, "orbit": "GTO", "site": "CCSFS SLC 40", "gridfins": False, "reused": False, "legs": False},
    {"flight": 50,  "payload": 3000, "orbit": "ISS", "site": "VAFB SLC 4E", "gridfins": True,  "reused": False, "legs": True},
])

print("\n🔎 New data for prediction:")
print(new_data)

# --- Step 3: Predict ---
predictions = model.predict(new_data)

# --- Step 4: Interpret results ---
results = ["✅ Success 🚀" if p == 1 else "❌ Fail 💥" for p in predictions]

print("\n📊 Prediction results:")
for i, res in enumerate(results):
    print(f"Launch {i+1}: {res}")

# --- Step 5: Save results to CSV ---
output_df = new_data.copy()
output_df["prediction"] = predictions
output_df["result"] = results

os.makedirs("data", exist_ok=True)
output_path = os.path.join("data", "predictions.csv")
output_df.to_csv(output_path, index=False)

print(f"\n💾 Predictions saved to {output_path}")
