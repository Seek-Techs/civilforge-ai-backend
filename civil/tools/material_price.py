from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool

search = DuckDuckGoSearchRun()

@tool
def get_current_material_price(material: str, unit: str = "") -> str:
    """Fetch latest market price in Nigeria (Lagos preferred) for construction materials in Naira.
    Examples: cement per bag, 12mm rebar per ton, sharp sand per trip, granite per ton."""
    query = f"current price {material} {unit} Lagos Nigeria 2026 Naira market rate site:.ng OR site:jumia.com.ng OR site:konga.com"
    result = search.run(query)
    return f"Search result for {material} ({unit}): {result}"