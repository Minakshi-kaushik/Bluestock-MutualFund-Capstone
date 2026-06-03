# Mutual Fund Warehouse Platform Data Dictionary (Day 2 Deliverable)

## Dimension Tables Reference Maps

### `dim_fund`
* `amfi_code` (INTEGER, Primary Key): Unique AMFI Identification asset index key.
* `scheme_name` (TEXT, Not Null): Public tracking asset tag name.
* `fund_house` (TEXT): Parent asset management company system group.
* `category` (TEXT): Asset grouping strategy assignment tiering.
* `plan` (TEXT): Direct or Regular asset channels.
* `risk_category` (TEXT): Core risk matrix categorization scale marker.
* `sebi_category_code` (TEXT): SEBI standard mapping classification string.

### `dim_date`
* `date_id` (TEXT, Primary Key): Unique date representation structured as `YYYY-MM-DD`.
* `calendar_year` (INTEGER): Gregorian tracking calendar extraction year scalar.
* `calendar_month` (INTEGER): Month number reference (1-12).
* `calendar_day` (INTEGER): Day of month index.
* `day_of_week` (TEXT): Weekday name string (e.g., Monday).
* `is_weekend` (INTEGER): Logical binary indicator validation checklist (0=False, 1=True).

## Core Transactional Metrics Fact Tables

### `fact_transactions`
* `transaction_id` (INTEGER, Primary Key Autoincrement): Core ledger sequence surrogate key.
* `investor_id` (TEXT): Masked client unique identity string.
* `transaction_date` (TEXT, Foreign Key -> dim_date): Date assignment index pointer.
* `amfi_code` (INTEGER, Foreign Key -> dim_fund): Fund mapping relational linker.
* `transaction_type` (TEXT): Operational transaction categorization: `SIP`, `Lumpsum`, `Redemption`.
* `amount_inr` (REAL): Net localized capital value executed.
* `state` / `city` / `city_tier` / `age_group` / `gender` / `annual_income_lakh` / `payment_mode`: Demographic and operational tracking metadata attributes.
* `kyc_status` (TEXT): Compliance check constraint enum values: `Verified`, `Pending`, `Failed`.

### `fact_nav`
* `nav_id` (INTEGER, Primary Key Autoincrement): Internal layout row surrogate index.
* `amfi_code` (INTEGER, Foreign Key -> dim_fund): Targeted asset reference identification key.
* `date_id` (TEXT, Foreign Key -> dim_date): Operational historical tracking date.
* `nav` (REAL): Net Asset Value price matrix entry.

### `fact_performance`
* `performance_id` (INTEGER, Primary Key Autoincrement): Core internal sequence tracking key.
* `amfi_code` (INTEGER, Foreign Key -> dim_fund): Target fund schema identifier.
* `return_1yr_pct` / `return_3yr_pct` / `return_5yr_pct` / `benchmark_3yr_pct` (REAL): Calculated historic annual return variables.
* `alpha` / `beta` / `sharpe_ratio` / `sortino_ratio` (REAL): Advanced risk assessment coefficients.
* `expense_ratio_pct` (REAL): Annual fund operational maintenance asset cost.
* `expense_anomaly_flag` (INTEGER): Validation exception logic trigger (1 if outside 0.1% - 2.5% parameters, else 0).

### `fact_aum`
* `aum_id` (INTEGER, Primary Key Autoincrement): Surrogate identifier key.
* `date_id` (TEXT, Foreign Key -> dim_date): Associated date key.
* `fund_house` (TEXT): Target asset management group string.
* `aum_crore` (REAL): Aggregated total managed capital pool expressed in Crore INR.
* `num_schemes` (INTEGER): Count of structural active funds under administration.