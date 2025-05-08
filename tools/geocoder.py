from langchain.tools import Tool

def geocode():
    pass

GeocoderTool = Tool(
    name="Geocoder",
    func=geocode,
    description=""
)
