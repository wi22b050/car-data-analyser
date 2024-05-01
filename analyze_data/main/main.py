"""
API-CarDataAnalyzer
"""
from visualise_data import DataVisualizer
from analyze_data import AnalyseCarData

from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from fastapi import FastAPI


app = FastAPI(title="API-CAR-ANALYSIS", description="Analyse car data", version="1", docs_url="/docs")


@app.get("/get-model-counts-comparison/", response_class=StreamingResponse)
async def get_model_counts_diagram():
    df = AnalyseCarData().combined_df
    visualizer = DataVisualizer(df)
    image_bytes = visualizer.plot_model_counts()
    
    # This creates a generator that will yield the image bytes
    def iterfile():  
        yield image_bytes
    
    return StreamingResponse(iterfile(), media_type="image/png")

@app.get("/get-price-distribution/", response_class=StreamingResponse)
async def get_price_distribution_diagram():
    df = AnalyseCarData().combined_df
    visualizer = DataVisualizer(df)
    image_bytes = visualizer.plot_price_distribution()
    
    def iterfile():
        yield image_bytes
    
    return StreamingResponse(iterfile(), media_type="image/png")

@app.get("/get-average-price-comparison/", response_class=StreamingResponse)
async def get_average_price_comparison_diagram():
    df = AnalyseCarData().combined_df
    visualizer = DataVisualizer(df)
    image_bytes = visualizer.plot_average_price_comparison()
    
    def iterfile():
        yield image_bytes
    
    return StreamingResponse(iterfile(), media_type="image/png")

@app.get("/get-price-difference-accross-ds/", response_class=StreamingResponse)
async def get_price_difference_accross_datasets():
    df = AnalyseCarData().combined_df
    visualizer = DataVisualizer(df)
    image_bytes = visualizer.plot_price_difference_comparison()
    
    def iterfile():
        yield image_bytes
    
    return StreamingResponse(iterfile(), media_type="image/png")
