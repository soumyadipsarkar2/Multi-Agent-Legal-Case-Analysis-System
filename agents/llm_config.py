from langchain.llms import Ollama

def get_llm():
    return Ollama(base_url="http://localhost:11434", model="llama3")
