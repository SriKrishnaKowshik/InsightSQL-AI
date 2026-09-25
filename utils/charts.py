import pandas as pd
import plotly.express as px


class ChartGenerator:
    """
    Automatically creates Plotly charts based on
    the returned DataFrame.
    """

    @staticmethod
    def create_chart(df: pd.DataFrame):

        if df is None or df.empty:
            return None

        columns = list(df.columns)

        # Need at least 2 columns for visualization
        if len(columns) < 2:
            return None

        first_col = columns[0].lower()
        second_col = columns[1]

        # ==================================================
        # Monthly Revenue Trend
        # ==================================================
        if "month" in first_col:

            fig = px.line(
                df,
                x=columns[0],
                y=columns[1],
                markers=True,
                title="Monthly Revenue Trend"
            )

            fig.update_traces(
                line_color="#2563EB",
                line_width=3,
                marker_size=8
            )

            fig.update_layout(
                template="plotly_white",
                title_x=0,
                xaxis_title="Month",
                yaxis_title="Revenue (€)"
            )

            return fig

        # ==================================================
        # Category Revenue
        # ==================================================
        if "category" in first_col:

            fig = px.bar(
                df,
                x=columns[0],
                y=columns[1],
                text=columns[1],
                title="Revenue by Category"
            )

            fig.update_traces(
                marker_color="#2563EB",
                texttemplate="€%{text:,.0f}",
                textposition="outside"
            )

            fig.update_layout(
                template="plotly_white",
                showlegend=False,
                title_x=0
            )

            return fig

        # ==================================================
        # Product Revenue
        # ==================================================
        if "product" in first_col:

            fig = px.bar(
                df,
                x=columns[0],
                y=columns[1],
                text=columns[1],
                title="Top Products by Revenue"
            )

            fig.update_traces(
                marker_color="#2563EB",
                texttemplate="€%{text:,.0f}",
                textposition="outside"
            )

            fig.update_layout(
                template="plotly_white",
                showlegend=False,
                title_x=0
            )

            return fig

        # ==================================================
        # Customers by City
        # ==================================================
        if "city" in first_col:

            fig = px.bar(
                df,
                x=columns[1],
                y=columns[0],
                orientation="h",
                text=columns[1],
                title="Customers by City"
            )

            fig.update_traces(
                marker_color="#2563EB",
                textposition="outside"
            )

            fig.update_layout(
                template="plotly_white",
                showlegend=False,
                title_x=0,
                xaxis_title="Customers",
                yaxis_title=""
            )

            return fig

        # ==================================================
        # Payment Distribution
        # ==================================================
        if "payment" in first_col:

            fig = px.pie(
                df,
                names=columns[0],
                values=columns[1],
                hole=0.45,
                title="Payment Method Distribution"
            )

            fig.update_layout(
                template="plotly_white",
                title_x=0
            )

            return fig

        # ==================================================
        # Generic Numeric Chart
        # ==================================================
        if pd.api.types.is_numeric_dtype(df[columns[1]]):

            fig = px.bar(
                df,
                x=columns[0],
                y=columns[1],
                text=columns[1],
                title="Analysis Result"
            )

            fig.update_traces(
                marker_color="#2563EB",
                textposition="outside"
            )

            fig.update_layout(
                template="plotly_white",
                showlegend=False,
                title_x=0
            )

            return fig

        return None