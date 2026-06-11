import pandas as pd
import os


def recommend_funds(risk_appetite):

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    scorecard_path = os.path.join(
        project_root, "data", "processed", "fund_scorecard.csv"
    )

    if not os.path.exists(scorecard_path):
        return f"File not found: {scorecard_path}"

    df = pd.read_csv(scorecard_path)

    # Risk mapping based on Sharpe ranges
    # (since risk_grade column doesn't exist)

    appetite = risk_appetite.strip().title()

    if appetite == "Low":
        recommendations = df.sort_values(
            by=["Sharpe Ratio", "Max Drawdown"], ascending=[False, True]
        ).head(3)

    elif appetite == "Moderate":
        recommendations = df.sort_values(by=["Fund Score"], ascending=False).head(3)

    elif appetite == "High":
        recommendations = df.sort_values(
            by=["3Yr CAGR", "Sharpe Ratio"], ascending=False
        ).head(3)

    else:
        return "Invalid input. Choose Low, Moderate, or High."

    return recommendations[
        ["Fund Name", "3Yr CAGR", "Sharpe Ratio", "Alpha", "Fund Score"]
    ]


if __name__ == "__main__":
    print("=" * 60)
    print("MUTUAL FUND RECOMMENDATION ENGINE")
    print("=" * 60)

    risk = input("\nEnter Risk Appetite (Low/Moderate/High): ")

    result = recommend_funds(risk)

    print("\nTop 3 Recommended Funds\n")
    print(result.to_string(index=False))

