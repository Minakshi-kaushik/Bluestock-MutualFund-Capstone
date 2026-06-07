import sqlite3
import numpy as np
import pandas as pd
from pathlib import Path


def run_advanced_risk_pipeline():
    print(" Initializing Day 6 Advanced Risk Pipeline...")

    # Resolve project directory paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / "bluestock_mf.db"
    OUTPUT_CSV = BASE_DIR / "data" / "processed" / "advanced_risk_metrics.csv"

    if not DB_PATH.exists():
        print(f"❌ Error: Database not found at {DB_PATH}")
        return

    # 1. Fetch historical raw NAV timeline from database
    with sqlite3.connect(DB_PATH) as conn:
        query = """
        SELECT n.date_id as Date, f.scheme_name as Scheme, n.nav as NAV 
        FROM fact_nav n
        INNER JOIN dim_fund f ON n.amfi_code = f.amfi_code;
        """
        df_raw = pd.read_sql_query(query, conn)

    # Pivot into a continuous price matrix
    nav_matrix = (
        df_raw.pivot(index="Date", columns="Scheme", values="NAV").ffill().bfill()
    )

    # Calculate daily percentage returns
    returns_matrix = nav_matrix.pct_change().dropna()

    # Assume the first scheme in the alpha list acts as our benchmark index proxy if none is specified
    benchmark_col = returns_matrix.columns[0]

    risk_records = []

    # 2. Compute quantitative risk metrics for each scheme
    for scheme in returns_matrix.columns:
        fund_returns = returns_matrix[scheme].values
        bench_returns = returns_matrix[benchmark_col].values

        if len(fund_returns) < 30:
            continue  # Skip assets with insufficient data points

        # Value at Risk (Historical 95% Confidence)
        var_95 = np.percentile(fund_returns, 5)

        # Conditional Value at Risk (Expected Shortfall below 95% VaR)
        tail_losses = fund_returns[fund_returns <= var_95]
        cvar_95 = tail_losses.mean() if len(tail_losses) > 0 else var_95

        # Static Lifetime Beta for structural comparison
        covariance = np.cov(fund_returns, bench_returns)[0][1]
        bench_variance = np.var(bench_returns)
        lifetime_beta = covariance / bench_variance if bench_variance != 0 else 1.0

        # 60-Day Rolling Beta calculation to capture historical drift
        df_pair = pd.DataFrame({"Fund": fund_returns, "Bench": bench_returns})
        rolling_cov = df_pair["Fund"].rolling(window=60).cov(df_pair["Bench"])
        rolling_var = df_pair["Bench"].rolling(window=60).var()
        rolling_beta_series = rolling_cov / rolling_var
        latest_rolling_beta = rolling_beta_series.iloc[-1]

        # Fall back to lifetime beta if the rolling series contains NaN due to window constraints
        if np.isnan(latest_rolling_beta):
            latest_rolling_beta = lifetime_beta

        risk_records.append(
            {
                "Fund Name": scheme,
                "Daily VaR 95%": abs(var_95),
                "Daily CVaR 95%": abs(cvar_95),
                "Lifetime Beta": lifetime_beta,
                "Latest 60_Day Rolling Beta": latest_rolling_beta,
            }
        )

    # 3. Export results to data/processed
    df_risk = pd.DataFrame(risk_records)
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df_risk.to_csv(OUTPUT_CSV, index=False)
    print(f" Success: Advanced Risk Matrix exported to {OUTPUT_CSV}")


if __name__ == "__main__":
    run_advanced_risk_pipeline()
