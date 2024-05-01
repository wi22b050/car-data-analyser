"""
API-CarDataAnalyzer
"""
from visualise_data import DataVisualizer
from analyze_data import AnalyseCarData

from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Query


app = FastAPI(title="API-CAR-ANALYSIS", description="Analyse car data", version="1", docs_url="/docs")


@app.get("/get-model-counts-comparison/", response_class=StreamingResponse,
          description=""" The bar charts reveal the count of the BMW models listen in company data versus web data. Each chart shows the distribution frequency of these models as recorded in two separate data sets. 
In the company data, the distribution of model is evenly spread among the four models. The web data reveals a different pattern, the 3er-Reihe is notably the most listed model, while the X1 and X3 show considerably fewer listings. """)
async def get_model_counts_diagram():
    df = AnalyseCarData().combined_df
    visualizer = DataVisualizer(df)
    image_bytes = visualizer.plot_model_counts()
    
    # This creates a generator that will yield the image bytes
    def iterfile():  
        yield image_bytes
    
    return StreamingResponse(iterfile(), media_type="image/png")

@app.get("/get-price-distribution/", response_class=StreamingResponse,
          description="""The box plots display the distribution of prices for the BMW models (X3, 5er-Reihe, 3er-Reihe, X1) across three years (2020, 2022, 2023) (rose for 2020, purple for 2022 and darker purple for 2023). 
Across all models, a general upward trend in median prices from 2020 to 2023 is observed. The X1 model maintains a relatively consistent pricing structure throughout the three years, with only a modest increase, while the X3 model experiences a significant price surge in 2023, setting it apart from earlier years. There are several outliers across different models and years. The 3er-Reihe shows particularly high variability and numerous outliers, suggesting a wide range of prices within this model.""")
async def get_price_distribution_diagram():
    df = AnalyseCarData().combined_df
    visualizer = DataVisualizer(df)
    image_bytes = visualizer.plot_price_distribution()
    
    def iterfile():
        yield image_bytes
    
    return StreamingResponse(iterfile(), media_type="image/png")

@app.get("/get-average-price-comparison/", response_class=StreamingResponse,
          description="""The bar chart compares the average prices of the BMW models (X3, 5er-Reihe, 3er-Reihe, X1) sourced from a car dealer and the web (willhaben.at). Each model has two bars representing the average price according to the car dealer (blue) and web (orange) sources.
Across all models, the web source tends to report higher average prices than the car dealer. The X3 and 5er-Reihe show significant differences in average prices between the two sources.
""")
async def get_average_price_comparison_diagram():
    df = AnalyseCarData().combined_df
    visualizer = DataVisualizer(df)
    image_bytes = visualizer.plot_average_price_comparison()
    
    def iterfile():
        yield image_bytes
    
    return StreamingResponse(iterfile(), media_type="image/png")

@app.get("/get-price-difference-accross-ds/", response_class=StreamingResponse,
         description="""The diagram illustrates price variances for the four BMW models across different fuel types (Diesel, Hybrid, Benzin). Each model and fuel type combination shows the average price difference between the two data sets. The black lines on the graph represent the range of maximum price differences for identical cars of the same model and fuel type. 
Diesel variants of the 5er-Reihe and X3 show a significant downward price difference, indicating they are cheaper on one platform compared to the other. Hybrid models, particularly in the 3er-Reihe and X3, exhibit smaller price differences. Benzin models show varied price differences with some extremes. Notably, the X3 show significant downward price difference. 
Additionally, the graph shows that the range of price differences is quite extensive for the X3 and 5er-Reihe models with Benzin fuel type, while it is relatively low for the 3er-Reihe model with Hybrid fuel type.""")
async def get_price_difference_accross_datasets():
    df = AnalyseCarData().combined_df
    visualizer = DataVisualizer(df)
    image_bytes = visualizer.plot_price_difference_comparison()
    
    def iterfile():
        yield image_bytes
    
    return StreamingResponse(iterfile(), media_type="image/png")
