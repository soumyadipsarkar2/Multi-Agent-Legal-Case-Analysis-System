from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from agents.tools import TOOLS
from agents.llm_config import get_llm
from agents.guardrails import flag_high_risk
from agents.evaluator import evaluate_summary

# 1. Prompt template
template = """
You are a multi-agent legal analysis system. Tools available:
{tools}

Use this format:
Question: {{input}}
Thought: step-by-step plan
Action: which tool to use
Action Input: input for that tool
Observation: result
...
Final Answer: your response
"""

prompt = PromptTemplate(template=template, input_variables=["input","tools"])
llm = get_llm()
chain = LLMChain(llm=llm, prompt=prompt)

# 2. Initialize agent
agent = ZeroShotAgent(llm_chain=chain, tools=TOOLS, verbose=False)
executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=TOOLS, llm=llm)

def analyze(text: str):
    # Run multi-agent pipeline
    formatted = "\n".join(f"- {t.name}: {t.description}" for t in TOOLS)
    summary = executor.run({"input": text, "tools": formatted})
    # Apply guardrails
    risks = flag_high_risk(text)
    # Dummy evaluation
    score = evaluate_summary(summary, text)
    return {"summary": summary, "high_risk": risks, "eval_score": score}
