from langchain.tools import Tool

def geocode(query: str) -> tuple(float, float):
    pass

GeocoderTool = Tool(
    name="Geocoder",
    func=geocode,
    description=""
)
