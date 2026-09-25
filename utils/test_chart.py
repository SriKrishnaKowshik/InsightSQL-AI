import pandas as pd

from utils.charts import ChartGenerator

df = pd.DataFrame({
    "product_name": [
        "Keyboard",
        "Mouse",
        "Webcam",
        "USB Hub",
        "Chair"
    ],
    "revenue": [
        650000,
        600000,
        500000,
        340000,
        280000
    ]
})

fig = ChartGenerator.create_chart(df)

fig.show()