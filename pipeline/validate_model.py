import sys, os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from datetime import datetime

# ✅ Ensure Python can find scripts/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --- Step 1: Load model ---
model_path = os.path.join("models", "random_forest_model.joblib")
model = joblib.load(model_path)
print(f"✅ Loaded model from {model_path}")

# --- Step 2: Load external validation dataset ---
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
validation_path = os.path.join(base_dir, "data", "validation", "validation_dataset.csv")
df_val = pd.read_csv(validation_path)

# --- Step 3: Separate features & target ---
X_val = df_val[["flight", "payload", "orbit", "site", "gridfins", "reused", "legs"]]
y_val = df_val["success"]

print(f"🔎 Validation dataset loaded: {X_val.shape[0]} samples")

# --- Step 4: Predict ---
y_pred = model.predict(X_val)
report = classification_report(y_val, y_pred)

# --- Step 5: Save validation report ---
os.makedirs("reports", exist_ok=True)
report_path = os.path.join("reports", "validation.txt")
with open(report_path, "w") as f:
    f.write(f"Validation Report - {datetime.now()}\n\n")
    f.write(report)

print(f"📄 Validation report saved at {report_path}")

# --- Step 6: Confusion Matrix ---
cm = confusion_matrix(y_val, y_pred)

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Oranges",
            xticklabels=["Fail", "Success"],
            yticklabels=["Fail", "Success"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix - Validation Dataset")
plt.tight_layout()

# Save confusion matrix as image
cm_path = os.path.join("reports", "validation_confusion_matrix.png")
plt.savefig(cm_path)
plt.close()

print(f"📊 Confusion matrix saved at {cm_path}")

# --- Step 7: Save predictions to CSV ---
os.makedirs("data", exist_ok=True)
pred_path = os.path.join("data", "validation_predictions.csv")

output_df = X_val.copy()
output_df["true"] = y_val
output_df["prediction"] = y_pred
output_df["result"] = ["✅ Success 🚀" if p == 1 else "❌ Fail 💥" for p in y_pred]

output_df.to_csv(pred_path, index=False)
print(f"💾 Validation predictions saved at {pred_path}")
