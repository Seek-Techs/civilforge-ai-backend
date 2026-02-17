from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

@tool
def get_current_price(material: str) -> str:
    """Get latest price in Nigeria (Naira) for civil materials"""
    query = f"current price of {material} in Nigeria 2026 per bag OR per ton OR per m3 site:ng"
    return search.run(query)