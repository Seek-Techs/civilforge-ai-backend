import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

class BOQItemSchema(BaseModel):
    item: str
    quantity: float
    unit: str
    unit_rate_naira: float
    total_naira: float

class BOQOutput(BaseModel):
    items: List[BOQItemSchema]
    grand_total_naira: float
    confidence: float = Field(..., ge=0, le=1)
    risks: List[str]

def boq_agent(project_description: str) -> BOQOutput:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a senior Nigerian Quantity Surveyor expert in Lagos market rates 2026. "
                   "Estimate realistic quantities, use current Naira rates, return ONLY valid JSON matching the schema. "
                   "Include 5-15% contingency in risks if uncertainty high."),
        ("human", "Project description: {description}\n\nGenerate complete BOQ."),
    ])

    chain = prompt | llm.with_structured_output(BOQOutput)
    return chain.invoke({"description": project_description})