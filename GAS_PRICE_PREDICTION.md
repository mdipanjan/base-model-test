# **Gas Price Prediction Model: Full Plan**

## **Step 1: Exploratory Data Analysis (EDA)**

### **1.1. Load and Inspect the Data**

- Convert **hex values to decimal** (e.g., `gas_price`, `gas_used`).
- Convert **timestamps** (if available) to `datetime`.
- Ensure **data types are correct** (integers for gas price, gas used, etc.).

### **1.2. Handle Missing Values**

- **`max_priority_fee_per_gas` & `max_fee_per_gas`** → If missing, set to `0` (common in legacy transactions).
- **`effective_gas_price`** → Use `gas_price` if it's missing.
- **Drop null `chain_id`** if multi-chain is not considered.

### **1.3. Data Visualization**

- **Gas Price Distribution** → Histogram of `gas_price` over transactions.
- **Time-Series Trend** → Plot `gas_price` per block to see trends.
- **Block Congestion vs. Gas Price** → Scatter plot `cumulative_gas_used` vs. `gas_price`.

---

## **Step 2: Feature Engineering**

To improve predictions, create meaningful **features**:

### **2.1. Time-Based Features**

✅ **Block Lag Features**:

- `gas_price_last_5_avg` → Rolling mean of the last 5 blocks.
- `gas_price_last_10_avg` → Rolling mean of last 10 blocks.
- `gas_price_change_5_blocks` → Change in `gas_price` over last 5 blocks.

✅ **Gas Fee Features**:

- **Normalized Gas Price** → `gas_price / max_fee_per_gas`
- **Priority Tip Ratio** → `max_priority_fee_per_gas / max_fee_per_gas`

✅ **Block Congestion Metrics**:

- **Gas Used Per Block** → Sum of `gas_used` for all TXs in a block.
- **Gas Utilization Ratio** → `gas_used / gas`

✅ **Transaction-Level Metrics**:

- **Transaction Index** → Position of TX in a block (`transaction_index`).
- **Failed TX Ratio** → `% of failed TXs per block`.

✅ **Day & Hour Features**:

- **Hour of the Day** (gas price fluctuates daily).
- **Day of the Week** (weekends are cheaper).

---

## **Step 3: Model Selection**

We need a model that handles **time-series prediction**.

### **3.1. Model Options**

| Model                    | Pros                                     | Cons                                    |
| ------------------------ | ---------------------------------------- | --------------------------------------- |
| **XGBoost/LightGBM**     | Handles tabular data well, fast training | Needs careful feature engineering       |
| **LSTM (Deep Learning)** | Captures sequential dependencies         | Requires more data, slower training     |
| **ARIMA/SARIMAX**        | Good for simple time trends              | Struggles with non-linear relationships |

👉 **First, train XGBoost, then test LSTM if needed.**

---

## **Step 4: Model Training**

### **4.1. Data Preparation**

- Train-Test Split → 80% Train, 20% Test.
- **Normalize Features** → Scale gas price, gas used, priority fees.
- **Create Lags** → Use past values as features.

### **4.2. Train XGBoost**

```python
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Split data
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train XGBoost
model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.05)
model.fit(X_train, y_train)

# Predict & Evaluate
y_pred = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, y_pred))
```

---

## **Step 5: Predictions & Deployment**

### **5.1. Predict Next Block’s Gas Price**

- Use the last 10 blocks to **forecast the next block’s gas price**.

### **5.2. Deploy as API**

- Serve predictions via **FastAPI**.
- Fetch live data & update every **block**.

---

## **Final Output**

✅ **Live Gas Price Forecast for Next Block**  
✅ **Helps users avoid high fees**  
✅ **Optimized transactions based on congestion**

---

### **Next Steps**

1️⃣ **Run EDA & visualize gas price trends**  
2️⃣ **Generate time-based features**  
3️⃣ **Train XGBoost** and evaluate accuracy  
4️⃣ **Deploy predictions to an API**

Let me know where you want to start! 🚀
