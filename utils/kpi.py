import pandas as pd
from pandas.api.types import is_numeric_dtype


class KPIGenerator:

    @staticmethod
    def generate(df: pd.DataFrame):

        if df.empty:
            return []

        cols = list(df.columns)
        lower = [c.lower() for c in cols]

        # -----------------------------
        # Numeric columns only
        # -----------------------------
        numeric_cols = [c for c in cols if is_numeric_dtype(df[c])]

        # =====================================================
        # REVENUE KPI
        # =====================================================
        revenue_col = next(
            (c for c in cols if "revenue" in c.lower() or "amount" in c.lower()),
            None,
        )

        if revenue_col is not None:

            total = float(df[revenue_col].sum())
            best = df.iloc[0]

            if "product_name" in lower:
                return [
                    ("Total Revenue", f"€{total:,.0f}"),
                    ("Best Product", str(best["product_name"])),
                    ("Highest Revenue", f"€{best[revenue_col]:,.0f}"),
                ]

            if "category_name" in lower:
                return [
                    ("Total Revenue", f"€{total:,.0f}"),
                    ("Top Category", str(best["category_name"])),
                    ("Highest Revenue", f"€{best[revenue_col]:,.0f}"),
                ]

            if "month" in lower:
                return [
                    ("Total Revenue", f"€{total:,.0f}"),
                    ("Best Month", str(best["month"])),
                    ("Average Month", f"€{df[revenue_col].mean():,.0f}"),
                ]

            if "first_name" in lower and "last_name" in lower:
                name = f"{best['first_name']} {best['last_name']}"
                return [
                    ("Total Revenue", f"€{total:,.0f}"),
                    ("Top Customer", name),
                    ("Highest Spend", f"€{best[revenue_col]:,.0f}"),
                ]

        # =====================================================
        # COUNT KPI (cities, countries, payments)
        # =====================================================
        count_col = next(
            (
                c
                for c in numeric_cols
                if any(
                    x in c.lower()
                    for x in ["count", "customer_count", "customers", "transactions"]
                )
            ),
            None,
        )

        if count_col is not None:

            total = int(df[count_col].sum())
            best = df.iloc[0]

            if "country" in lower:
                return [
                    ("Total Customers", f"{total:,}"),
                    ("Top Country", str(best["country"])),
                    ("Countries", str(len(df))),
                ]

            if "city" in lower:
                return [
                    ("Total Customers", f"{total:,}"),
                    ("Largest City", str(best["city"])),
                    ("Cities", str(len(df))),
                ]

            if "payment_method" in lower:
                return [
                    ("Transactions", f"{total:,}"),
                    ("Most Used", str(best["payment_method"])),
                    ("Methods", str(len(df))),
                ]

        # =====================================================
        # SINGLE NUMERIC COLUMN
        # =====================================================
        if len(numeric_cols) == 1:

            c = numeric_cols[0]

            return [
                ("Total", f"{df[c].sum():,.0f}"),
                ("Average", f"{df[c].mean():,.1f}"),
                ("Rows", str(len(df))),
            ]

        # =====================================================
        # SINGLE TEXT COLUMN
        # =====================================================
        if len(cols) == 1:
            return [
                ("Results", str(len(df))),
                ("First Item", str(df.iloc[0, 0])),
                ("Column", cols[0].replace("_", " ").title()),
            ]

        # =====================================================
        # DEFAULT
        # =====================================================
        return [
            ("Rows", str(len(df))),
            ("Columns", str(len(cols))),
            ("First Value", str(df.iloc[0, 0])),
        ]