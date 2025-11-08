# ContextForge 🔬

**Privacy-Preserving Multi-Agent Research Gap Detector**

ContextForge is a PhD-level multi-agent system that combines differential privacy with simulated Model Context Protocol (MCP) to identify research gaps, conduct agent debates, and generate novel hypotheses with 24-hour buildable MVP proposals.

## Features

🔐 **Privacy-First Architecture**
- Differential privacy using Laplace mechanism (configurable ε)
- DP-protected embeddings for all document processing
- Privacy-preserving agent-to-agent communication

🤖 **Multi-Agent Reasoning**
- **GapDetector**: Identifies research gaps and limitations
- **Debater**: Conducts pro/con debates on identified gaps
- **HypoGenerator**: Generates novel hypotheses and MVP proposals
- **Evolver**: Scores and ranks hypotheses iteratively

🔄 **Simulated MCP Protocol**
- Secure context passing between agents
- Message history tracking with privacy metadata
- DP noise injection in context envelopes

📊 **Comprehensive Reporting**
- Markdown reports with gaps, debates, and hypotheses
- JSON artifacts with reasoning traces
- Graphviz visualizations of agent debate trees

## Quick Start

1. **Upload Research Papers**
   - Supports PDF, DOCX, and TXT formats
   - Upload papers on any research domain

2. **Configure Privacy & Agents**
   - Set privacy budget (ε): Lower = more privacy, Higher = more accuracy
   - Choose number of agent iterations (1-5)
   - Select LLM model (gpt-4o-mini, gpt-4o, gpt-3.5-turbo)

3. **Run Analysis**
   - Watch agents debate via MCP protocol in real-time
   - Review identified gaps and generated hypotheses
   - Download GapForge Report with actionable MVPs

## Example Use Cases

**AI Safety Research**
- Find gaps in multilingual jailbreak datasets
- Generate privacy-preserving benchmark proposals
- Identify cross-dialect safety testing opportunities

**Biomedical AI**
- Drug repurposing hypothesis generation
- Privacy-preserving clinical trial analysis
- RNA folding gap detection

**General Research**
- Literature gap identification
- Cross-domain opportunity discovery
- 24-hour MVP proposal generation

## Sample Data

Use the included `sample_research.txt` to test the system. It contains summaries of:
- AI co-scientist research (multi-agent debates for hypothesis evolution)
- Algoverse AI safety research (low-compute artifacts and benchmarks)

Both documents include pre-identified gaps in privacy preservation and multilingual safety.

## Technical Stack

- **Framework**: Streamlit (UI), LangGraph (agent orchestration)
- **LLM**: OpenAI (configurable model)
- **Privacy**: diffprivlib (Laplace mechanism for DP)
- **Document Processing**: LangChain, PyPDF2, python-docx
- **Visualization**: Graphviz

## Privacy Guarantees

ContextForge implements differential privacy at two levels:

1. **Embedding Privacy**: Document embeddings are perturbed with DP noise before agent processing
2. **MCP Privacy**: Agent-to-agent context passing includes DP noise in message envelopes

The privacy budget (ε) controls the noise level:
- **ε = 0.1-0.5**: Strong privacy, more noise in outputs
- **ε = 1.0**: Balanced privacy/utility (default)
- **ε = 2.0-5.0**: Less noise, higher accuracy

## Architecture

```
User Upload → Document Processor (DP) → Multi-Agent System (MCP+DP) → Report Generator
                      ↓                           ↓
              Privacy Layer              GapDetector → Debater → HypoGenerator → Evolver
                (ε-DP)                        ↓           ↓            ↓             ↓
                                        MCP Messages with DP protection
```

## Future Enhancements

- Real MCP integration from Anthropic's open standard
- Decentralized multi-party simulation (federated agents)
- D3.js interactive visualization
- Web search integration for real-time gap validation
- Domain-specific adapters (biomedicine, AI safety)

## License

MIT License - Feel free to use, modify, and extend for your research!

---

**Built with privacy and ethics at the core** 🔐
