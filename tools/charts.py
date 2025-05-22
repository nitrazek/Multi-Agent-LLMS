from langchain_core.tools import tool
from pydantic import BaseModel, Field
from datetime import datetime
from os import makedirs
from os.path import join, dirname, abspath, exists
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")

class ChartInput(BaseModel):
    title: str = Field(description="Chart title")
    labels: list[str] = Field(description="Labels for the x-axis")
    values: list[float] = Field(description="Values for the y-axis")

@tool(
    "ChartTool",
    description="Generate and save a chart for given data. Returns the path to the saved chart image.",
    args_schema=ChartInput
)
def create_chart(title: str, labels: list[str], values: list[float]) -> str:
    plt.figure(figsize=(8, 4))
    plt.bar(labels, values)
    plt.title(title)
    plt.xlabel("Kategoria")
    plt.ylabel("Wartość")
    
    charts_dir_path = join(dirname(abspath(__file__)), "generated_charts")
    if not exists(charts_dir_path):
        makedirs(charts_dir_path)        
    
    chart_path = join(charts_dir_path, f"chart_{datetime.now().strftime("%Y%m%d%H%M%S")}.png")
    plt.savefig(chart_path)
    plt.close()
    
    return chart_path
