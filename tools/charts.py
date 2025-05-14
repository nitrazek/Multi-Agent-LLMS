from langchain_core.tools import tool
from pydantic import BaseModel, Field
import matplotlib.pyplot as plt
import tempfile
import os

class ChartInput(BaseModel):
    title: str = Field(description="Chart title")
    labels: list[str] = Field(description="Labels for the x-axis")
    values: list[float] = Field(description="Values for the y-axis")

@tool(
    "ChartTool",
    description="Generate and save a chart for given data. Returns the path to the saved chart image.",
    args_schema=ChartInput
)
def create_chart(title: str, labels: list[str], values: list[float]):
    plt.figure(figsize=(8, 4))
    plt.bar(labels, values)
    plt.title(title)
    plt.xlabel("Kategoria")
    plt.ylabel("Wartość")
    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(tmpfile.name)
    plt.close()
    return {"chart_path": tmpfile.name}