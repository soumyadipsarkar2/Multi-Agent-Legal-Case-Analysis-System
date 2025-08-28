## Multi‑Agent Legal Case Analysis System

A lightweight multi‑agent system for legal document analysis built on FastAPI and LangChain. It orchestrates multiple tools backed by an Ollama‑served LLM (default: `llama3`) to generate a summary, flag high‑risk clauses, and return a simple evaluation score.

### Key Features
- **FastAPI API**: Single POST endpoint at `/analyze`.
- **LangChain Agent Orchestration**: Zero‑shot agent with tool usage.
- **Pluggable Tools**: General legal and contract advice tools.
- **Guardrails**: Keyword‑based high‑risk flagging.
- **Evaluation Stub**: Simple length‑ratio score (replace with ROUGE/BERTScore).
- **Container/K8s Ready**: Dockerfile and Kubernetes manifests included.

## Architecture

- `app.py`: FastAPI app exposing `/analyze`.
- `orchestrator.py`: Builds the LangChain agent and executes the analysis pipeline.
- `agents/llm_config.py`: LLM provider (Ollama endpoint and model).
- `agents/tools.py`: LangChain `Tool` definitions used by the agent.
- `agents/guardrails.py`: Simple keyword‑based risk flagging.
- `agents/evaluator.py`: Placeholder evaluation metric.
- `k8s/`: Deployment and Service manifests.
- `Dockerfile`: Container build instructions.

Data flow:
1) Client sends a document to `/analyze`.
2) `orchestrator.analyze` formats tool descriptions and runs the agent.
3) The agent may call available tools to produce a final summary.
4) Guardrails flag high‑risk keywords from the original document.
5) Evaluator computes a simple score vs. the original text.
6) API responds with `{ summary, high_risk, eval_score }`.

## Requirements

- Python 3.10+
- `pip`
- [Ollama](https://ollama.com) running locally (default base URL: `http://localhost:11434`)
- Model: `llama3` (default; configurable in `agents/llm_config.py`)

## Quick Start (Local)

1) Install and start Ollama with the model:
```bash
brew install ollama  # macOS, or see Ollama docs for your OS
ollama serve &
ollama pull llama3
```

2) Create and activate a virtual environment, then install deps:
```bash
cd /Users/soumyadipsarkar/Multi-Agent-Legal-Case-Analysis-System
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

3) Run the API:
```bash
uvicorn app:app --reload --port 8000
```

4) Test the endpoint:
```bash
curl -sS -X POST \
  http://localhost:8000/analyze \
  -H 'Content-Type: application/json' \
  -d '{"document": "This Agreement includes an indemnify clause and termination for convenience."}' | jq
```

### Example Request
```json
{
  "document": "This Agreement includes an indemnify clause and termination for convenience."
}
```

### Example Response
```json
{
  "summary": "...model-generated summary...",
  "high_risk": ["indemnify", "termination for convenience"],
  "eval_score": 0.73
}
```

## Configuration

- LLM settings live in `agents/llm_config.py`:
  - Base URL: `http://localhost:11434`
  - Model: `llama3`

Update to point to a remote Ollama instance or a different model:
```python
# agents/llm_config.py
from langchain.llms import Ollama

def get_llm():
    return Ollama(base_url="http://your-ollama-host:11434", model="llama3:instruct")
```

## Project Layout

- `app.py`: FastAPI API (request/response models and `/analyze`).
- `orchestrator.py`: Builds `ZeroShotAgent` and `AgentExecutor`, runs pipeline.
- `agents/tools.py`: `LegalAdvisor` and `ContractAdvisor` tool functions.
- `agents/guardrails.py`: `HIGH_RISK_KEYWORDS` and `flag_high_risk` helper.
- `agents/evaluator.py`: `evaluate_summary` placeholder.
- `k8s/deployment.yaml`, `k8s/service.yaml`: Example manifests.
- `Dockerfile`: Production container build.
- `requirements.txt`: Python dependencies.

## Run with Docker

1) Build the image:
```bash
cd /Users/soumyadipsarkar/Multi-Agent-Legal-Case-Analysis-System
docker build -t legalpulse:latest .
```

2) Ensure Ollama is reachable from the container (default host network on macOS/Windows differs; consider using `host.docker.internal`). If your `agents/llm_config.py` points at `http://localhost:11434`, you may need to change it to `http://host.docker.internal:11434` when running in Docker on macOS/Windows.

3) Run the container:
```bash
docker run --rm -p 8000:8000 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  legalpulse:latest
```

Note: The code currently reads the base URL/model from code, not env vars. Either bake the setting into the image or update `llm_config.py` to read `OLLAMA_BASE_URL`/`OLLAMA_MODEL`.

## Deploy to Kubernetes

1) Push your image to a registry and update the deployment manifest image reference.

2) Apply manifests:
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

3) Verify and port‑forward if using a ClusterIP service:
```bash
kubectl get pods,svc
kubectl port-forward svc/legalpulse 8000:80
```

4) Call the API as usual:
```bash
curl -sS -X POST http://localhost:8000/analyze \
  -H 'Content-Type: application/json' \
  -d '{"document": "..."}'
```

## Development

- Code style: keep functions small and descriptive; avoid deep nesting.
- To add tools, extend `agents/tools.py` by adding more `Tool` instances.
- Replace the evaluator with a proper metric (ROUGE/BERTScore) as needed.
- Consider parameterizing LLM settings via environment variables.

### Running Tests
Tests are not included. Suggested direction:
- Add unit tests for `flag_high_risk` and `evaluate_summary`.
- Mock the LLM when testing agent execution.
- Use `pytest` and `httpx` for API tests.

## Security and Privacy

- Do not treat outputs as legal advice. For educational/demo use only.
- Input documents may contain sensitive data. Handle storage and logging responsibly.
- When exposing publicly, add authentication, rate limiting, and request size limits.

## Troubleshooting

- "Connection refused to Ollama": Ensure `ollama serve` is running and the base URL in `agents/llm_config.py` is reachable from your runtime (host/container/K8s).
- "Model not found": Run `ollama pull llama3` (or your selected model).
- Empty `summary` or odd outputs: Increase model context/temperature, refine prompt, or switch models.

## License

This project is provided as‑is without warranty. Add your preferred license here.
