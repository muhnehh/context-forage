# ContextForge - Privacy-Preserving Multi-Agent Research Gap Detector

## Overview
ContextForge is a PhD-level multi-agent system that combines differential privacy with simulated Model Context Protocol (MCP) to identify research gaps, conduct agent debates, and generate novel hypotheses with 24-hour buildable MVP proposals. The system processes research papers and outputs actionable insights while maintaining privacy guarantees.

**Current State**: Fully functional MVP with Streamlit interface, 4 specialized agents, and privacy-preserving architecture.

## Recent Changes (2025-11-08)
- Implemented complete multi-agent system with LangGraph orchestration
- Created privacy layer using diffprivlib for differential privacy
- Built simulated MCP protocol for secure agent context passing
- Developed 4 specialized agents: GapDetector, Debater, HypoGenerator, Evolver
- Implemented document processing with DP-protected embeddings
- Created comprehensive report generation with Markdown, JSON, and Graphviz visualization
- Built Streamlit UI with real-time agent debate streaming
- **Privacy Fix**: Wired epsilon slider to DocumentProcessor and MultiAgentSystem
- **Privacy Fix**: MCP apply_privacy flag now properly triggers DP noise in context envelopes

## Project Architecture

### Core Components

1. **privacy_layer.py**
   - Implements differential privacy using Laplace mechanism
   - Perturbs embeddings with configurable epsilon
   - Creates MCP envelopes for secure context passing
   - Privacy budget: ε=1.0 (configurable)

2. **document_processor.py**
   - Loads PDF, DOCX, TXT files using LangChain
   - Chunks documents using RecursiveCharacterTextSplitter
   - Generates embeddings via OpenAI with DP protection
   - Returns processed documents with privacy-protected embeddings

3. **mcp_simulator.py**
   - Simulates Model Context Protocol for agent communication
   - Manages context store and message history
   - Wraps agent data in privacy-preserving envelopes
   - Tracks all inter-agent communications

4. **agents.py**
   - Multi-agent system orchestrated via LangGraph StateGraph
   - 4 specialized agents:
     - **GapDetector**: Identifies research gaps and limitations
     - **Debater**: Conducts pro/con debates on gaps
     - **HypoGenerator**: Generates hypotheses and MVP proposals
     - **Evolver**: Scores and ranks hypotheses (novelty, feasibility, impact)
   - Iterative refinement: 3-5 evolution cycles
   - MCP-based context sharing between agents

5. **report_generator.py**
   - Generates comprehensive Markdown reports
   - Exports JSON artifacts with reasoning traces
   - Creates Graphviz visualizations of agent debate trees
   - Provides downloadable outputs

6. **app.py**
   - Streamlit interface with document upload
   - Real-time agent progress tracking
   - Interactive results display (gaps, debates, hypotheses)
   - Privacy & MCP protocol analytics
   - Report download functionality

### Agent Workflow
```
GapDetector → Debater → HypoGenerator → Evolver → (iterate) → Finalize
     ↓           ↓            ↓              ↓
   MCP Messages passed with DP protection
```

### Key Features
- **Privacy-First**: All embeddings perturbed with differential privacy
- **MCP Protocol**: Simulated secure context passing between agents
- **Multi-Agent Debates**: Pro/con analysis of research gaps
- **Hypothesis Evolution**: Iterative refinement with scoring
- **24h MVP Proposals**: Actionable research ideas with implementation plans
- **Comprehensive Reports**: Markdown + JSON + visualization outputs

## Tech Stack
- **Framework**: Streamlit (UI), LangGraph (agent orchestration)
- **LLM**: OpenAI (gpt-4o-mini default, configurable)
- **Privacy**: diffprivlib (Laplace mechanism for DP)
- **Document Processing**: LangChain, PyPDF2, python-docx
- **Visualization**: Graphviz
- **Embeddings**: OpenAI embeddings with DP protection

## Environment Variables
- `OPENAI_API_KEY`: Required for LLM and embeddings
- `SESSION_SECRET`: Available for session management

## Usage
1. Upload research papers (PDF/DOCX/TXT)
2. Configure agent iterations and privacy budget (ε)
3. Run multi-agent analysis
4. Review gaps, debates, and hypotheses
5. Download GapForge Report (Markdown/JSON)

## Example Use Cases
- **AI Safety**: Find gaps in multilingual jailbreak datasets, privacy-preserving benchmarks
- **Biomedical AI**: Drug repurposing hypotheses, RNA folding gap detection
- **General Research**: Literature gap identification, cross-domain opportunities

## Sample Data
- `sample_research.txt`: Contains summaries of AI co-scientist and Algoverse research with identified gaps

## Next Steps (Future Enhancements)
- Real MCP integration from Anthropic's open standard
- Decentralized multi-party simulation (federated agents)
- D3.js interactive visualization
- Web search integration for real-time gap validation
- Domain-specific adapters (biomedicine, AI safety)

## User Preferences
- Focus on privacy-preserving, ethical AI applications
- Emphasis on actionable, 24-hour buildable MVPs
- Interest in biomedicine (RNA, drug repurposing) and AI safety
