import pandas as pd
import os

# ── Paths ──────────────────────────────────────────────────────────────────
RAW_PATH     = r"C:\Users\UTD\OneDrive\Documents\supply-chain-analytics\data\raw\DataCoSupplyChainDataset.csv"
CLEANED_PATH = r"C:\Users\UTD\OneDrive\Documents\supply-chain-analytics\data\cleaned\supply_chain_cleaned.csv"

# ── Load ───────────────────────────────────────────────────────────────────
print("Loading data...")
df = pd.read_csv(RAW_PATH, encoding='latin-1')
print(f"Raw shape: {df.shape}")

# ── Drop useless columns ───────────────────────────────────────────────────
drop_cols = [
    'Customer Email', 'Customer Password', 'Customer Street',
    'Customer Zipcode', 'Order Zipcode', 'Product Description',
    'Product Image'
]
df.drop(columns=drop_cols, inplace=True)

# ── Clean column names ─────────────────────────────────────────────────────
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_', regex=False)
    .str.replace(r'[^\w]', '_', regex=True)
    .str.replace(r'_+', '_', regex=True)
    .str.strip('_')
)

# ── Fix date columns ───────────────────────────────────────────────────────
df['order_date'] = pd.to_datetime(df['order_date_dateorders'], errors='coerce')
df['shipping_date'] = pd.to_datetime(df['shipping_date_dateorders'], errors='coerce')
df.drop(columns=['order_date_dateorders', 'shipping_date_dateorders'], inplace=True)

# ── Handle missing values ──────────────────────────────────────────────────
print(f"\nMissing values before:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
df.dropna(subset=['order_date', 'shipping_date'], inplace=True)
df.fillna({'product_status': 0}, inplace=True)
df.dropna(inplace=True)
print(f"\nMissing values after:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

# ── Remove duplicates ──────────────────────────────────────────────────────
before = len(df)
df.drop_duplicates(inplace=True)
print(f"\nDuplicates removed: {before - len(df)}")

# ── Derived columns ────────────────────────────────────────────────────────
df['shipping_delay_days'] = (df['shipping_date'] - df['order_date']).dt.days
df['is_late'] = (df['shipping_delay_days'] > df['days_for_shipping_real']).astype(int)
df['order_year']  = df['order_date'].dt.year
df['order_month'] = df['order_date'].dt.month
df['order_quarter'] = df['order_date'].dt.quarter

# ── Save ───────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(CLEANED_PATH), exist_ok=True)
df.to_csv(CLEANED_PATH, index=False)
print(f"\n Cleaned data saved to: {CLEANED_PATH}")
print(f"Final shape: {df.shape}")
print(f"\nColumns:\n{list(df.columns)}")