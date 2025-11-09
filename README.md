# ContextForge 🔬

**Privacy-Preserving Multi-Agent Research Gap Detector with Real MCP Communication**

A sophisticated system that uses multiple AI agents to analyze research documents, identify gaps in the literature, debate findings, generate novel hypotheses, and evolve research proposals—all while maintaining differential privacy.

## Features ✨

- 🤖 **4-Stage Multi-Agent Pipeline**
  - Gap Detector: Identifies research gaps
  - Debater: Critiques and debates findings
  - Hypothesis Generator: Creates novel hypotheses
  - Evolution Agent: Refines proposals

- 🔐 **Privacy-Preserving**
  - Differential Privacy (Laplace mechanism)
  - Privacy-preserving inter-agent communication
  - Epsilon-configurable privacy levels

- 📨 **Real MCP Protocol**
  - Actual inter-agent message passing
  - Unique message IDs and timestamps
  - Privacy metadata tracking

- ⚡ **Local-Only LLM**
  - Ollama integration (mistral model)
  - No API keys required
  - Fully private on your machine

- 🌐 **Web Interface**
  - Streamlit dashboard
  - Document upload support
  - Interactive results visualization

## Quick Start 🚀

### Prerequisites
- Python 3.11+
- Ollama installed and running: `ollama serve`
- Mistral model: `ollama pull mistral`

### Setup

```bash
# Clone the repository
git clone https://github.com/muhnehh/context-forage.git
cd context-forage

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Visit: **http://127.0.0.1:8501**

## System Architecture

```
User Upload (PDF/Text)
        ↓
Document Processor (HuggingFace embeddings)
        ↓
Stage 1: Gap Detector Agent (CrewAI + Ollama)
        ↓
Stage 2: Debater Agent (Critique & Analysis)
        ↓
Stage 3: Hypothesis Generator (Novel Ideas)
        ↓
Stage 4: Evolution Agent (Refinement)
        ↓
Results Dashboard (Gaps, Debates, Hypotheses)
```

## Technology Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| CrewAI | 0.28.0+ | Multi-agent orchestration |
| Ollama | Latest | Local LLM inference |
| Streamlit | Latest | Web UI |
| LangChain | Latest | Document processing |
| HuggingFace | Latest | Embeddings |
| NumPy | Latest | Privacy computations |

## Usage

1. **Settings Tab**: Configure privacy level (epsilon) and model selection
2. **Upload & Analyze Tab**: Upload research documents and run analysis
3. **Results Tabs**: View identified gaps, debates, hypotheses, and MCP messages

## Key Files

- `agents.py` - 4-agent multi-agent system
- `app.py` - Streamlit web interface
- `mcp_simulator.py` - Real MCP protocol implementation
- `privacy_layer.py` - Differential privacy layer
- `document_processor.py` - Document processing pipeline

## Configuration

### Privacy Settings
- `epsilon` (default: 1.0) - Privacy budget (lower = more private)
- Higher epsilon = less noise, lower privacy

### Model Selection
- Mistral (default, faster)
- LLaMA2
- Other Ollama models

## Testing

Run the test suite:
```bash
python test_real_mcp.py
```

<img width="1098" height="751" alt="image" src="https://github.com/user-attachments/assets/0cfc0002-e56d-49d4-aa68-022274cc80dd" />
<img width="1099" height="793" alt="image" src="https://github.com/user-attachments/assets/193a7bf3-53f9-408d-95ab-f97f481cc465" />

It produces an output in pdf format:
[ContextForge_Analysis_20251109_141448.pdf](https://github.com/user-attachments/files/23439157/ContextForge_Analysis_20251109_141448.pdf)

## Performance

- First run: ~2-3 minutes (model loading)
- Subsequent runs: ~1-2 minutes (cached)
- Gap detection: ~30 seconds
- Full 4-stage analysis: ~1-2 minutes

## License

MIT License - See LICENSE file for details

## Author

**muhnehh** - [GitHub](https://github.com/muhnehh)

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## Status

✅ **PRODUCTION READY**
- All core features working
- Real MCP communication verified
- Privacy layer functional
- Web UI operational

---

**Start analyzing research gaps now!** 🎉
