import pandas as pd
from sqlalchemy import create_engine, text

# ── Config ─────────────────────────────────────────────────────────────────
DB_USER     = "postgres"
DB_PASSWORD = "admin123"
DB_HOST     = "localhost"
DB_PORT     = "5432"
DB_NAME     = "supply_chain"

CLEANED_PATH = r"C:\Users\UTD\OneDrive\Documents\supply-chain-analytics\data\cleaned\supply_chain_cleaned.csv"

# ── Connect ─────────────────────────────────────────────────────────────────
print("Connecting to PostgreSQL...")
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# ── Load cleaned CSV ────────────────────────────────────────────────────────
print("Loading cleaned CSV...")
df = pd.read_csv(CLEANED_PATH, parse_dates=['order_date', 'shipping_date'])
print(f"Rows to load: {len(df)}")

# ── Create schema ───────────────────────────────────────────────────────────
with engine.connect() as conn:
    conn.execute(text("""
        DROP TABLE IF EXISTS orders;
        CREATE TABLE orders (
            type                        VARCHAR(20),
            days_for_shipping_real      INT,
            days_for_shipment_scheduled INT,
            benefit_per_order           NUMERIC(10,2),
            sales_per_customer          NUMERIC(10,2),
            delivery_status             VARCHAR(50),
            late_delivery_risk          INT,
            category_id                 INT,
            category_name               VARCHAR(100),
            customer_city               VARCHAR(100),
            customer_country            VARCHAR(100),
            customer_fname              VARCHAR(100),
            customer_id                 INT,
            customer_lname              VARCHAR(100),
            customer_segment            VARCHAR(50),
            customer_state              VARCHAR(100),
            department_id               INT,
            department_name             VARCHAR(100),
            latitude                    NUMERIC(10,6),
            longitude                   NUMERIC(10,6),
            market                      VARCHAR(50),
            order_city                  VARCHAR(100),
            order_country               VARCHAR(100),
            order_customer_id           INT,
            order_id                    INT,
            order_item_cardprod_id      INT,
            order_item_discount         NUMERIC(10,2),
            order_item_discount_rate    NUMERIC(5,4),
            order_item_id               INT,
            order_item_product_price    NUMERIC(10,2),
            order_item_profit_ratio     NUMERIC(5,4),
            order_item_quantity         INT,
            sales                       NUMERIC(10,2),
            order_item_total            NUMERIC(10,2),
            order_profit_per_order      NUMERIC(10,2),
            order_region                VARCHAR(100),
            order_state                 VARCHAR(100),
            order_status                VARCHAR(50),
            product_card_id             INT,
            product_category_id         INT,
            product_name                VARCHAR(200),
            product_price               NUMERIC(10,2),
            product_status              INT,
            shipping_mode               VARCHAR(50),
            order_date                  TIMESTAMP,
            shipping_date               TIMESTAMP,
            shipping_delay_days         INT,
            is_late                     INT,
            order_year                  INT,
            order_month                 INT,
            order_quarter               INT
        );
    """))
    conn.commit()
print(" Table created.")

# ── Insert data ─────────────────────────────────────────────────────────────
print("Loading data into PostgreSQL (this may take ~30 seconds)...")
df.to_sql('orders', engine, if_exists='append', index=False, chunksize=5000)
print(" Data loaded!")

# ── Verify ──────────────────────────────────────────────────────────────────
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM orders;"))
    count = result.fetchone()[0]
    print(f"\n Total rows in database: {count}")