# SpaceX Capstone Project – Machine Learning & MLOps

Este proyecto implementa un **pipeline completo de Machine Learning con MLOps**, usando:

- **Python + scikit-learn** para el modelo de predicción.
- **Makefile** para automatizar tareas básicas (entrenar, evaluar, predecir, validar).
- **DVC (Data Version Control)** para versionar datasets, modelos y métricas de manera profesional.

El objetivo es predecir si la primera etapa de un cohete Falcon 9 aterrizará con éxito.

---

## Estructura del proyecto

```
spacex-capstone-project/
│── data/
│   ├── processed/clean_dataset.csv       # Dataset principal (entrenamiento)
│   ├── validation/validation_dataset.csv # Dataset externo (validación)
│── models/
│   └── random_forest_model.joblib        # Modelo entrenado (versionado con DVC)
│── reports/
│   ├── evaluation.txt                    # Reporte de evaluación
│   ├── evaluation_confusion_matrix.png   # Matriz de confusión (evaluación)
│   ├── validation.txt                    # Reporte de validación
│   ├── validation_confusion_matrix.png   # Matriz de confusión (validación)
│── pipeline/
│   ├── train_model.py                    # Script de entrenamiento
│   ├── evaluate_model.py                 # Script de evaluación
│   ├── predict.py                        # Script de predicción
│   ├── validate_model.py                 # Script de validación externa
│── Makefile                              # Automatización simple
│── dvc.yaml                              # Pipeline definido en DVC
│── dvc.lock                              # Hashes/versionado de outputs
│── requirements.txt
│── README.md
```

---

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/Tarik2012/spacex-capstone-project.git
cd spacex-capstone-project
```

2. Crea el entorno virtual e instala dependencias:

```bash
python -m venv env
source env/bin/activate   # Linux/Mac
env\Scripts\activate      # Windows

pip install -r requirements.txt
```

3. Inicializa DVC:

```bash
dvc init
```

---

## Uso con **Makefile**

El `Makefile` automatiza los pasos básicos del pipeline:

```bash
# Entrenar el modelo
make train

# Evaluar el modelo en test interno
make evaluate

# Predecir en lote
make predict

# Validar en dataset externo
make validate

# Ejecutar todo el pipeline en orden
make all
```

---

## Uso con **DVC**

DVC permite versionar datasets y modelos, y ejecutar el pipeline de manera reproducible.

### 📌 Definición del pipeline (dvc.yaml)

- **train** → dataset limpio + script → modelo `.joblib`
- **evaluate** → modelo + script → reporte `.txt` + matriz `.png`
- **predict** → modelo + script → predicciones `.csv`
- **validate** → modelo + script → validación `.txt` + `.png` + predicciones `.csv`

Ejecuta todo el pipeline:

```bash
dvc repro
```

Ver el DAG de dependencias:

```bash
dvc dag
```

Ver estado del pipeline:

```bash
dvc status
```

---

## Versionado de modelos y datasets con DVC

- Cada vez que el dataset o los scripts cambian, DVC detecta el cambio y reentrena el modelo.
- Aunque los archivos en `models/` y `reports/` se sobrescriben, **DVC guarda todas las versiones en cache**.
- Puedes volver a cualquier versión con:

```bash
git checkout <commit>
dvc checkout
```

---

## Outputs principales

1. **Modelo entrenado**

   - `models/random_forest_model.joblib`

2. **Evaluación interna**

   - `reports/evaluation.txt`
   - `reports/evaluation_confusion_matrix.png`

3. **Predicciones en lote**

   - `data/predictions.csv`

4. **Validación externa**
   - `reports/validation.txt`
   - `reports/validation_confusion_matrix.png`
   - `data/validation_predictions.csv`

---

## Autor

Proyecto desarrollado por **Tarik Errochdi**  
 Granada, España  
 Objetivo: Convertirme en Data Scientist / MLOps Engineer
