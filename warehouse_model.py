import duckdb
import pandas as pd

print("Initializing local Data Warehouse simulation via DuckDB...")

# 1. Establish Warehouse Connection
con = duckdb.connect(database='celigo_warehouse.db')

# 2. CREATE RAW LANDING LAYER
con.execute("DROP TABLE IF EXISTS raw_crm_leads;")
con.execute("""
    CREATE TABLE raw_crm_leads (
        id VARCHAR,
        lead_name VARCHAR,
        company_name VARCHAR,
        status VARCHAR,
        created_date DATE,
        qualified_date DATE,
        estimated_deal_value INT
    );
""")

# Injecting realistic enterprise data matching our analytical hypotheses
con.execute("""
    INSERT INTO raw_crm_leads VALUES 
    ('00Q51', 'Thomas Wooknam', 'Canvas Data', 'Qualified', '2026-05-01', '2026-05-18', 50000),   
    ('00Q52', 'Sarah Jenkins', 'Celigo Partner', 'In Progress', '2026-05-10', NULL, 30000),      
    ('00Q53', 'John Doe', 'Legacy Corp', 'Qualified', '2026-05-18', '2026-05-18', 120000),       
    ('00Q54', 'Jane Smith', 'SaaS Startup', 'Qualified', '2026-05-20', '2026-05-15', 45000);     
""")

# 3. BUILD THE DATA MART LAYER WITH ADVANCED SQL LOGIC
con.execute("DROP TABLE IF EXISTS mart_pipeline_analytics;")
con.execute("""
    CREATE TABLE mart_pipeline_analytics AS 
    WITH hypothesis_validation_layer AS (
        SELECT 
            id AS lead_id,
            lead_name,
            company_name,
            status AS lead_status,
            created_date,
            qualified_date,
            estimated_deal_value,
            COALESCE(date_diff('day', created_date, qualified_date), 0) AS days_to_qualify,
            
            CASE 
                WHEN created_date > qualified_date THEN 'SYSTEM_OVERWRITE_CORRUPTION'
                WHEN created_date = qualified_date AND status = 'Qualified' THEN 'PROCESS_SHORTCUT_WARN'
                ELSE 'VALID_DATA_INTEGRITY'
            END AS data_integrity_flag
        FROM raw_crm_leads
    )
    SELECT 
        lead_id,
        lead_name,
        company_name,
        lead_status,
        created_date,
        estimated_deal_value,
        data_integrity_flag,
        days_to_qualify,
        
        CASE 
            WHEN data_integrity_flag = 'PROCESS_SHORTCUT_WARN' THEN NULL 
            ELSE days_to_qualify
        END AS true_velocity_days,
        
        CASE 
            WHEN data_integrity_flag = 'SYSTEM_OVERWRITE_CORRUPTION' THEN 0
            ELSE estimated_deal_value
        END AS validated_pipeline_revenue,
        
        200000 AS corporate_revenue_target
    FROM hypothesis_validation_layer;
""")

# 4. EXPORT FOR THE SELF-SERVE DASHBOARD LAYER
output_file = 'tableau_reporting_data.csv'
con.execute(f"COPY mart_pipeline_analytics TO '{output_file}' (HEADER, DELIMITER ',');")

print(f"Data Mart built successfully. Verified data exported to '{output_file}'.")
con.close()
