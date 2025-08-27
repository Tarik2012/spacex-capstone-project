# Variables
PYTHON = python
PIPELINE_DIR = pipeline
MODEL_FILE = models/random_forest_model.joblib

# Target por defecto → corre todo
all: train evaluate predict validate

# Entrenamiento: genera el modelo
train: $(PIPELINE_DIR)/train_model.py
	$(PYTHON) $(PIPELINE_DIR)/train_model.py

# Evaluación → guarda metrics & confusion matrix en reports/
evaluate: $(MODEL_FILE) $(PIPELINE_DIR)/evaluate_model.py
	$(PYTHON) $(PIPELINE_DIR)/evaluate_model.py

# Predicción en lote → puedes adaptar a que guarde CSV si lo deseas
predict: $(MODEL_FILE) $(PIPELINE_DIR)/predict.py
	$(PYTHON) $(PIPELINE_DIR)/predict.py

# Validación externa → guarda metrics & confusion matrix en reports/
validate: $(MODEL_FILE) $(PIPELINE_DIR)/validate_model.py
	$(PYTHON) $(PIPELINE_DIR)/validate_model.py

# Limpieza
clean:
	rm -f $(MODEL_FILE) reports/*.txt reports/*.png data/predictions.csv
