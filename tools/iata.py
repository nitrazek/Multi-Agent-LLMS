from langchain_core.tools import tool
from pydantic import BaseModel, Field
from airportsdata import load

airports = load('IATA')

class IATAInput(BaseModel):
    query: str = Field(description="Nazwa miasta lub lotniska do wyszukania kodu IATA.")

@tool(
    "IATAFinder",
    description="Znajdź kod IATA dla podanego miasta lub lotniska (None jeśli nie znaleziono).",
    args_schema=IATAInput
)
def find_iata(query: str) -> str | None:
    query_lower = query.lower()
    for code, data in airports.items():
        if query_lower in data['city'].lower() or query_lower in data['name'].lower():
            return code
    return None