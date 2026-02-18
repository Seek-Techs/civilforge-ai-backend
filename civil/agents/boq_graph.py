from typing import TypedDict, Annotated, List
import operator
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from .tools.material_price import get_current_material_price

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

class BOQItem(BaseModel):
    description: str = Field(..., description="Item name e.g. 'Cement - Dangote'")
    quantity: float
    unit: str = Field(..., description="e.g. bags, tons, m³, trips")
    unit_rate_naira: float = Field(..., description="Current market rate")
    total_naira: float

class BOQResult(BaseModel):
    items: List[BOQItem]
    sub_total_naira: float
    contingency_percent: float = Field(..., ge=5, le=20)
    grand_total_naira: float
    confidence: float = Field(..., ge=0, le=1)
    risks: List[str] = Field(default_factory=list)

parser = PydanticOutputParser(pydantic_object=BOQResult)

class AgentState(TypedDict):
    description: str
    messages: Annotated[list, operator.add]
    boq_result: dict | None

def extract_and_estimate(state: AgentState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a senior Nigerian Quantity Surveyor in Lagos 2026.
Extract realistic BOQ items from the project description.
Estimate quantities conservatively.
Do NOT guess prices — use the provided tool for that.
Output ONLY valid JSON matching this schema:\n{format_instructions}"""),
        MessagesPlaceholder("messages"),
        ("human", "{description}\n\n{format_instructions}"),
    ])

    chain = prompt | llm | parser

    try:
        result = chain.invoke({
            "description": state["description"],
            "format_instructions": parser.get_format_instructions(),
            "messages": state["messages"]
        })
        return {"boq_result": result.dict(), "messages": [AIMessage(content="Extracted initial BOQ (prices missing)")]}

    except Exception as e:
        return {"messages": [AIMessage(content=f"Extraction failed: {str(e)}")]}

def fetch_prices(state: AgentState):
    if not state.get("boq_result"):
        return state

    messages = state["messages"]
    for item in state["boq_result"]["items"]:
        price_info = get_current_material_price.invoke({
            "material": item["description"],
            "unit": item["unit"]
        })
        messages.append(AIMessage(content=f"Price info for {item['description']}: {price_info}"))

    return {"messages": messages}

def finalize_boq(state: AgentState):
    if not state.get("boq_result"):
        return state

    # Simple final prompt to incorporate prices and calculate
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You have item list and price search results. Fill in realistic unit rates, calculate totals, add 10-15% contingency, list 3-5 key risks. Return ONLY JSON matching schema."),
        MessagesPlaceholder("messages"),
        ("human", "Finalize BOQ.\n{format_instructions}"),
    ])

    chain = prompt | llm | parser

    result = chain.invoke({
        "messages": state["messages"],
        "format_instructions": parser.get_format_instructions()
    })

    return {"boq_result": result.dict()}

# Build graph
workflow = StateGraph(state_schema=AgentState)
workflow.add_node("extract", extract_and_estimate)
workflow.add_node("prices", fetch_prices)
workflow.add_node("finalize", finalize_boq)

workflow.set_entry_point("extract")
workflow.add_edge("extract", "prices")
workflow.add_edge("prices", "finalize")
workflow.add_edge("finalize", END)

graph = workflow.compile()