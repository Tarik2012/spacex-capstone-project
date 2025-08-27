import sys, os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from datetime import datetime

# ✅ Ensure Python can find scripts/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.preprocessing import load_and_preprocess

# --- Step 1: Load test data ---
X_train, X_test, y_train, y_test, preprocessor = load_and_preprocess()

# --- Step 2: Load the saved model ---
model_path = os.path.join("models", "random_forest_model.joblib")
model = joblib.load(model_path)
print(f"✅ Loaded model from {model_path}")

# --- Step 3: Evaluate on test set ---
y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred)

# --- Step 4: Save classification report ---
os.makedirs("reports", exist_ok=True)
report_path = os.path.join("reports", "evaluation.txt")
with open(report_path, "w") as f:
    f.write(f"Evaluation Report - {datetime.now()}\n\n")
    f.write(report)

print(f"📄 Evaluation report saved at {report_path}")

# --- Step 5: Confusion Matrix ---
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Fail", "Success"],
            yticklabels=["Fail", "Success"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix - Random Forest (Loaded Model)")
plt.tight_layout()

# Save confusion matrix as image
cm_path = os.path.join("reports", "evaluation_confusion_matrix.png")
plt.savefig(cm_path)
plt.close()

print(f"📊 Confusion matrix saved at {cm_path}")
