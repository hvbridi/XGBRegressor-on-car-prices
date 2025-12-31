# XGBRegressor-on-car-prices
# Used Car Price Prediction with XGBoost

## Project Overview
This project aims to predict the selling price of used vehicles based on features such as model, year, odometer reading, and manufacturer. The solution uses a **XGBoost Regressor**, optimized to balance accuracy and generalization, avoiding overfitting on a dataset with high cardinality features.

## Key Results
After extensive data preprocessing and hyperparameter tuning, the final model achieved:

| Metric | Value | Interpretation |
| :--- | :--- | :--- |
| **MAE (Mean Absolute Error)** | **~1,851.00** | On average, the prediction misses the real price by ~1.8k units. |
| **MAPE (Mean Absolute Percentage Error)** | **~15.7%** | The model has an average percentage error of around 15%. |

## Methodology

### 1. Data Cleaning & Preprocessing
* **Outlier Removal:** Filtered out unrealistic prices (e.g., `< 500` or `> 100,000`) to remove noise.
* **Imputation:** Used `SimpleImputer` (most frequent strategy) for missing values.
* **Encoding:**
    * `OneHotEncoder`: For low-cardinality categorical features (e.g., `fuel`, `type`).
    * `OrdinalEncoder`: For high-cardinality features (`model`), which proved more robust than Target Encoding for this specific dataset.

### 2. Model Configuration (The "Anti-Overfitting" Strategy)
I used **XGBoost** with a specific configuration to prevent the model from memorizing specific car instances:
* `max_depth=12`: To capture complex relationships.
* `subsample=0.7` & `colsample_bytree=0.7`: Randomly sampling rows and columns per tree to force the model to generalize.
* `n_estimators=5000` with `early_stopping`: To find the optimal number of trees.

---

## Experiments & Trade-offs

Here is a log of techniques tested but **not** to include in the final production model, and why:

### 1. Log-Transformation on Target (`np.log1p`)
* **Hypothesis:** Transforming the price to a logarithmic scale usually helps with skewed distributions and reduces the impact of expensive outliers.
* **Result:** Both MAE and MAPE **increased** (worsened) with the transformation.
* **Conclusion:** The price distribution in the filtered range (500-100k) was well-behaved enough that the log transformation added unnecessary complexity without performance gain. It was reverted to predicting raw prices.

### 2. Target Encoding on Car Models
* **Hypothesis:** Replacing the car model name with its average price would give the XGBoost a strong signal.
* **Result:** Massive Overfitting. The Training MAE dropped to ~200 (memorization), but Validation MAE increased to ~1920.
* **Conclusion:** The model became "unstable", relying too much on the average price of the car model and ignoring the specific condition (year/km) of the individual vehicle. `OrdinalEncoder` provided a better balance.

### 3. K-Fold Cross-Validation (in Final Pipeline)
* **Hypothesis:** Using 5-Fold or 10-Fold CV ensures the most robust error estimation.
* **Result:** While Cross-Validation was used during the **hyperparameter tuning phase** to find the best `max_depth` and `learning_rate`, it was removed from the final execution script.
* **Reason:** Given the large number of estimators (5000) and depth (12), running full CV takes significant computational time. For the final pipeline, a simple **Train/Validation Split** (with a fixed random seed) was sufficient to monitor the metrics and allow for faster iteration and deployment.

---

## How to Run

1. Clone this repository:
   ```bash
   git clone [https://github.com/hvbridi/XGBRegressor-on-car-prices.git](https://github.com/hvbridi/XGBRegressor-on-car-prices.git)
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute the notebook in the `notebooks/` folder.
---
*Developed by Henrique Varnier Bridi*