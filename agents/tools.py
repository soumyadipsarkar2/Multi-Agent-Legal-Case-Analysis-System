from langchain.agents import Tool
from .llm_config import get_llm

llm = get_llm()

def legal_advice_fn(text: str) -> str:
    prompt = f"Provide general legal advice on:\n{text}"
    return llm(prompt)

def contract_advice_fn(text: str) -> str:
    prompt = f"Provide contract-specific advice on:\n{text}"
    return llm(prompt)

TOOLS = [
    Tool(name="LegalAdvisor", func=legal_advice_fn,
         description="General legal questions."),
    Tool(name="ContractAdvisor", func=contract_advice_fn,
         description="Contract clause analysis.")
]
