import streamlit as st
import os
from document_processor import DocumentProcessor
from agents import MultiAgentSystem
from report_generator import ReportGenerator
import json
from datetime import datetime
import logging

# Suppress verbose logging for faster startup
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("crewai").setLevel(logging.WARNING)
logging.getLogger("langchain").setLevel(logging.WARNING)

# Configure logging for ContextForge only
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="ContextForge - Privacy-Preserving Research Gap Detector",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 ContextForge")
st.markdown("### Privacy-Preserving Multi-Agent Research Gap Detector")
st.markdown("*Powered by CrewAI + Ollama (FREE Local LLM) + OpenAlex + Differential Privacy*")

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")

st.sidebar.markdown("### 🤖 Multi-Agent Framework")
st.sidebar.markdown("**CrewAI** - Collaborative AI agents")
st.sidebar.markdown("**LangGraph** - Agent orchestration")

st.sidebar.markdown("### 🔓 FREE LLM Setup")
st.sidebar.markdown("""
Using **Ollama** - Local, free LLM
1. Download: https://ollama.ai
2. Install model: `ollama pull llama2`
3. Run: `ollama serve`

No API keys needed! ✨
""")

model_choice = st.sidebar.selectbox(
    "Ollama Model (must be running locally)",
    ["mistral", "llama2", "neural-chat", "dolphin-mixtral"],
    index=0,
    key="model_choice_select",
    help="Make sure the model is installed: ollama pull <model>"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📚 Built-in Frameworks
- **CrewAI**: Multi-agent collaboration
- **LangGraph**: Agent state management  
- **LangChain**: Document processing
- **OpenAlex API**: Free research data
- **HuggingFace**: Free embeddings
- **Streamlit + Plotly**: Interactive dashboard

### 🔐 Privacy Features
- Differential Privacy (DP) embeddings
- Privacy-preserving multi-agent communication
- MCP Protocol simulation
""")

# Main layout
st.markdown("---")

# Configuration sliders (global, available to all tabs)
col_iter, col_eps = st.columns(2)

with col_iter:
    max_iterations = st.slider(
        "Agent Iterations",
        min_value=1,
        max_value=10,
        value=3,
        key="max_iterations_slider",
        help="Number of evolutionary cycles for hypothesis refinement"
    )

with col_eps:
    epsilon = st.slider(
        "Privacy Budget (ε)",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1,
        key="privacy_epsilon_slider",
        help="Lower values = more privacy, higher values = more accuracy"
    )

st.markdown("---")

# Create tabs for different modes
tab1, tab2, tab3, tab4 = st.tabs([
    "📤 Upload & Analyze",
    "🔍 Research Papers",
    "📊 Visualizations",
    "ℹ️ About"
])

# TAB 1: Upload and Analyze
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📄 Upload Research Documents")
        st.markdown("Upload PDF, DOCX, or TXT files for analysis")
        
        uploaded_files = st.file_uploader(
            "Select files",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            help="Upload research papers or documents"
        )
    
    with col2:
        st.header("🎯 Research Goal")
        research_goal = st.text_area(
            "Optional: Guide the analysis",
            value="Identify research gaps in privacy and AI safety",
            height=120,
            help="Help the agents focus on specific areas"
        )
    
    if uploaded_files:
        st.success(f"✅ Loaded {len(uploaded_files)} document(s)")
        
        if st.button("🚀 Run CrewAI Multi-Agent Analysis", type="primary", width='stretch'):
            with st.spinner("🔄 Processing documents with differential privacy..."):
                try:
                    processor = DocumentProcessor(epsilon=epsilon)
                    processed_docs = []
                    
                    os.makedirs("temp_uploads", exist_ok=True)
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, uploaded_file in enumerate(uploaded_files):
                        status_text.text(f"Processing: {uploaded_file.name}")
                        
                        file_path = f"temp_uploads/{uploaded_file.name}"
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        try:
                            doc_data = processor.process_document(file_path)
                            processed_docs.append(doc_data)
                        except Exception as e:
                            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                        
                        progress_bar.progress((idx + 1) / len(uploaded_files))
                    
                    status_text.empty()
                    progress_bar.empty()
                
                    if processed_docs:
                        st.success("✅ Documents processed with DP-protected embeddings")
                        
                        with st.expander("📊 Document Processing Details"):
                            for doc in processed_docs:
                                st.markdown(f"**{doc['file_name']}**: {doc['num_chunks']} chunks, Privacy: ✓")
                        
                        st.markdown("---")
                        st.header("🤖 CrewAI Multi-Agent Analysis")
                        
                        with st.spinner("🧠 Initializing CrewAI agents..."):
                            try:
                                agent_system = MultiAgentSystem(
                                    model_name=model_choice,
                                    max_iterations=max_iterations,
                                    epsilon=epsilon
                                )
                                
                                st.info("🔄 CrewAI agents are analyzing via MCP protocol...")
                                
                                col_a, col_b, col_c, col_d = st.columns(4)
                                
                                with col_a:
                                    st.markdown("**🔍 GapDetector**")
                                    gap_status = st.empty()
                                
                                with col_b:
                                    st.markdown("**💬 Debater**")
                                    debate_status = st.empty()
                                
                                with col_c:
                                    st.markdown("**💡 HypoGenerator**")
                                    hypo_status = st.empty()
                                
                                with col_d:
                                    st.markdown("**🔄 Evolver**")
                                    evol_status = st.empty()
                                
                                gap_status.text("Starting...")
                                
                                final_state = agent_system.analyze(processed_docs, research_goal)
                                
                                gap_status.success(f"✓ {len(final_state['gaps'])} gaps")
                                debate_status.success(f"✓ {len(final_state['debates'])} debates")
                                hypo_status.success(f"✓ {len(final_state['final_hypotheses'])} hypotheses")
                                evol_status.success(f"✓ Complete")
                                
                            except Exception as e:
                                st.error(f"❌ Error initializing CrewAI: {str(e)}")
                                st.info("🔧 Make sure Ollama is running: `ollama serve` in another terminal")
                                st.info(f"⚠️ Check that the model is downloaded: `ollama pull {model_choice}`")
                                st.stop()
                        
                        st.success("✅ CrewAI analysis complete!")
                        
                        # Store in session state for other tabs
                        st.session_state['final_state'] = final_state
                        st.session_state['processed_docs'] = processed_docs
                        st.session_state['epsilon'] = epsilon
                        
                        st.markdown("---")
                        st.header("📋 Results")
                        
                        result_tab1, result_tab2, result_tab3, result_tab4 = st.tabs([
                            "🎯 Top Hypotheses",
                            "🔍 Research Gaps",
                            "💬 Agent Debates",
                            "🔐 Privacy & MCP"
                        ])
                        
                        with result_tab1:
                            st.subheader("Top Ranked Hypotheses & MVP Proposals")
                            
                            for i, hypo in enumerate(final_state.get('final_hypotheses', [])[:5], 1):
                                with st.expander(
                                    f"**Hypothesis {i}** - Score: {hypo.get('score', 0):.1f}/10",
                                    expanded=(i == 1)
                                ):
                                    st.markdown(f"**Gap:** {hypo['gap']}")
                                    st.markdown("**Proposal:**")
                                    st.markdown(hypo['proposal'])
                        
                        with result_tab2:
                            st.subheader("Identified Research Gaps")
                            for i, gap in enumerate(final_state.get('gaps', []), 1):
                                st.markdown(f"{i}. {gap}")
                        
                        with result_tab3:
                            st.subheader("Multi-Agent Debates")
                            
                            for i, debate in enumerate(final_state.get('debates', [])[:3], 1):
                                st.markdown(f"### Debate {i}")
                                st.markdown(f"**Gap:** {debate['gap']}")
                                
                                col_pro, col_con = st.columns(2)
                                with col_pro:
                                    st.markdown("**✅ Pro Arguments**")
                                    st.markdown(debate['pro_arguments'])
                                
                                with col_con:
                                    st.markdown("**⚠️ Challenges**")
                                    st.markdown(debate['con_arguments'])
                                
                                st.markdown("---")
                        
                        with result_tab4:
                            st.subheader("🔐 Privacy & MCP Protocol Analysis")
                            
                            col_m1, col_m2, col_m3 = st.columns(3)
                            
                            with col_m1:
                                st.metric("Privacy Budget (ε)", f"{epsilon}")
                                mcp_count = len(final_state.get('mcp_messages', []))
                                st.metric("✅ MCP Messages", mcp_count)
                            
                            with col_m2:
                                st.metric("Agent Actions", len(final_state.get('reasoning_trace', [])))
                                st.metric("Iterations", final_state.get('iteration', 0))
                            
                            with col_m3:
                                st.metric("DP-Protected Chunks", sum(d['num_chunks'] for d in processed_docs))
                                st.metric("Protocol", "MCP-DP-v1.0")
                            
                            st.markdown("---")
                            
                            # Real MCP Message History
                            mcp_messages = final_state.get('mcp_messages', [])
                            if mcp_messages:
                                st.success(f"✅ {len(mcp_messages)} REAL MCP Messages Exchanged Between Agents")
                                
                                with st.expander("� MCP Message History (REAL Inter-Agent Communication)", expanded=True):
                                    # Create a nice table of messages
                                    cols = st.columns([1, 1.5, 1.5, 1.2, 1, 1])
                                    with cols[0]:
                                        st.markdown("**#**")
                                    with cols[1]:
                                        st.markdown("**From Agent**")
                                    with cols[2]:
                                        st.markdown("**To Agent**")
                                    with cols[3]:
                                        st.markdown("**Protocol**")
                                    with cols[4]:
                                        st.markdown("**Privacy**")
                                    with cols[5]:
                                        st.markdown("**Status**")
                                    
                                    st.divider()
                                    
                                    for idx, msg in enumerate(mcp_messages, 1):
                                        cols = st.columns([1, 1.5, 1.5, 1.2, 1, 1])
                                        with cols[0]:
                                            st.text(f"{idx}")
                                        with cols[1]:
                                            st.markdown(f"🤖 {msg.get('from', '?')}")
                                        with cols[2]:
                                            st.markdown(f"→ {msg.get('to', '?')}")
                                        with cols[3]:
                                            st.code(msg.get('protocol', 'MCP'))
                                        with cols[4]:
                                            if msg.get('privacy_applied'):
                                                st.success("🔐 Yes")
                                            else:
                                                st.warning("No")
                                        with cols[5]:
                                            st.info(msg.get('status', 'ok'))
                                    
                                    st.divider()
                                    st.markdown("**Raw JSON Data:**")
                                    st.json(mcp_messages)
                            else:
                                st.info("No MCP messages (agents may be operating independently)")
                            
                            st.markdown("---")
                            
                            with st.expander("🔍 Reasoning Trace"):
                                st.json(final_state.get('reasoning_trace', []))
                        
                        st.markdown("---")
                        st.header("💾 Download GapForge Report")
                        
                        report_gen = ReportGenerator()
                        
                        col_r1, col_r2 = st.columns(2)
                        
                        with col_r1:
                            markdown_report = report_gen.generate_markdown_report(final_state)
                            st.download_button(
                                label="📄 Download Markdown Report",
                                data=markdown_report,
                                file_name=f"gapforge_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                mime="text/markdown",
                                width='stretch'
                            )
                        
                        with col_r2:
                            json_artifact = report_gen.generate_json_artifact(final_state)
                            st.download_button(
                                label="📊 Download JSON Artifact",
                                data=json.dumps(json_artifact, indent=2),
                                file_name=f"gapforge_artifact_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                mime="application/json",
                                width='stretch'
                            )
                        
                        st.success("✅ Analysis complete! Download your reports above.")
                
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
                    logger.exception("Analysis error")
    
    else:
        st.info("👆 Upload research documents to begin analysis")

# TAB 2: Research Papers (OpenAlex Integration)
with tab2:
    st.header("🔍 Search Research Papers (OpenAlex API)")
    st.info("📝 Use the 'Upload & Analyze' tab to upload your research documents")

# TAB 3: Visualizations
with tab3:
    st.header("📊 Analysis Results")
    
    if 'final_state' in st.session_state:
        state = st.session_state['final_state']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Gaps Found", len(state.get('gaps', [])))
        with col2:
            st.metric("Debates", len(state.get('debates', [])))
        with col3:
            st.metric("Hypotheses", len(state.get('hypotheses', [])))
        with col4:
            st.metric("MCP Messages", len(state.get('mcp_messages', [])))
        
        st.markdown("---")
        
        if state.get('gaps'):
            st.subheader("🎯 Identified Gaps")
            for i, gap in enumerate(state['gaps'], 1):
                st.write(f"{i}. {gap}")
        
        if state.get('hypotheses'):
            st.subheader("💡 Generated Hypotheses")
            for hyp in state['hypotheses']:
                with st.expander(hyp.get('proposal', 'Hypothesis')):
                    st.write(hyp.get('description', 'No description'))
                    if hyp.get('score'):
                        st.metric("Score", f"{hyp['score']:.1f}/10")
        
        if state.get('mcp_messages'):
            st.subheader("� MCP Messages Exchanged")
            st.metric("Total Messages", len(state['mcp_messages']))
            for msg in state['mcp_messages'][:5]:
                st.write(f"**{msg.get('from_agent')}** → **{msg.get('to_agent')}**")
    else:
        st.info("👈 Run an analysis first in the 'Upload & Analyze' tab to see results")


# TAB 4: About
with tab4:
    st.header("ℹ️ About ContextForge")
    
    st.markdown("""
    ### 🎯 Mission
    Privacy-preserving multi-agent research gap detector with completely FREE tools and frameworks.
    
    ### 🔧 Technology Stack
    
    **Multi-Agent Frameworks:**
    - **CrewAI** - Collaborative AI agents with role-based workflows
    - **LangGraph** - Stateful agent orchestration
    - **LangChain** - Document processing and utilities
    
    **Free LLM:**
    - **Ollama** - Local, free LLM inference
    - **LLaMA2** - Open-source language model
    - **Mistral** - Alternative models available
    
    **Document Processing:**
    - **HuggingFace Embeddings** - Free, open-source embeddings
    - **Sentence Transformers** - Privacy-preserving representations
    
    **Privacy:**
    - **Differential Privacy** - Formal privacy guarantees
    - **DiffPrivLib** - DP mechanism implementations
    - **Privacy Layer** - Custom privacy protections
    
    **Visualization:**
    - **Streamlit** - Interactive dashboard
    - **Plotly** - Interactive graphs
    - **Altair** - Declarative visualization
    
    **Research Data:**
    - **OpenAlex API** - Free academic research database
    
    ### ✨ Key Features
    
    1. **No API Keys** - Everything runs locally or uses free APIs
    2. **Multi-Agent Analysis** - CrewAI agents with specialized roles
    3. **Privacy-First** - Differential privacy on all embeddings
    4. **Interactive Dashboard** - Streamlit + Plotly visualizations
    5. **Research Data Integration** - OpenAlex for academic papers
    6. **24h MVP Proposals** - Actionable research ideas
    
    ### 🚀 Quick Start
    
    ```bash
    # 1. Install Ollama
    # https://ollama.ai
    
    # 2. Download a model
    ollama pull llama2
    
    # 3. Start Ollama
    ollama serve
    
    # 4. Install ContextForge
    pip install -r requirements.txt
    
    # 5. Run the app
    streamlit run app.py
    ```
    
    ### 📚 Documentation
    
    - [CrewAI Docs](https://docs.crewai.com/)
    - [LangGraph Docs](https://python.langchain.com/docs/langgraph/)
    - [Ollama GitHub](https://github.com/ollama/ollama)
    - [OpenAlex API](https://docs.openalex.org/)
    
    ### 🤝 Contributing
    
    This is an open-source project. Contributions welcome!
    
    ### 📄 License
    
    MIT License - Feel free to use and modify
    
    ---
    
    **ContextForge v2.0** | Built with ❤️ for research
    """)
    
    if uploaded_files:
        st.success(f"✅ Loaded {len(uploaded_files)} document(s)")
    
    if st.button("🚀 Run Multi-Agent Analysis", type="primary", width='stretch'):
        with st.spinner("🔄 Processing documents with differential privacy..."):
            processor = DocumentProcessor(epsilon=epsilon)
            processed_docs = []
            
            os.makedirs("temp_uploads", exist_ok=True)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing: {uploaded_file.name}")
                
                file_path = f"temp_uploads/{uploaded_file.name}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                try:
                    doc_data = processor.process_document(file_path)
                    processed_docs.append(doc_data)
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                
                progress_bar.progress((idx + 1) / len(uploaded_files))
            
            status_text.empty()
            progress_bar.empty()
        
        if processed_docs:
            st.success("✅ Documents processed with DP-protected embeddings")
            
            with st.expander("📊 Document Processing Details"):
                for doc in processed_docs:
                    st.markdown(f"**{doc['file_name']}**: {doc['num_chunks']} chunks, Privacy: ✓")
            
            st.markdown("---")
            st.header("🤖 Multi-Agent Reasoning")
            
            agent_progress = st.empty()
            reasoning_container = st.container()
            
            with st.spinner("🧠 Initializing multi-agent system..."):
                agent_system = MultiAgentSystem(
                    model_name=model_choice,
                    max_iterations=max_iterations,
                    epsilon=epsilon
                )
            
            with reasoning_container:
                st.info("🔄 Agents are debating via MCP protocol...")
                
                col_a, col_b, col_c, col_d = st.columns(4)
                
                with col_a:
                    st.markdown("**🔍 GapDetector**")
                    gap_status = st.empty()
                
                with col_b:
                    st.markdown("**💬 Debater**")
                    debate_status = st.empty()
                
                with col_c:
                    st.markdown("**💡 HypoGenerator**")
                    hypo_status = st.empty()
                
                with col_d:
                    st.markdown("**🔄 Evolver**")
                    evol_status = st.empty()
                
                gap_status.text("Running...")
                
                final_state = agent_system.run(processed_docs)
                
                gap_status.success(f"✓ {len(final_state['gaps'])} gaps")
                debate_status.success(f"✓ {len(final_state['debates'])} debates")
                hypo_status.success(f"✓ {len(final_state['hypotheses'])} hypotheses")
                evol_status.success(f"✓ {final_state['iteration']} iterations")
            
            st.success("✅ Multi-agent analysis complete!")
            
            st.markdown("---")
            st.header("📋 Results")
            
            tab1, tab2, tab3, tab4 = st.tabs([
                "🎯 Top Hypotheses",
                "🔍 Research Gaps",
                "💬 Agent Debates",
                "🔐 Privacy & MCP"
            ])
            
            with tab1:
                st.subheader("Top Ranked Hypotheses & MVP Proposals")
                
                for i, hypo in enumerate(final_state.get('final_hypotheses', [])[:5], 1):
                    with st.expander(
                        f"**Hypothesis {i}** - Score: {hypo.get('score', 0):.1f}/10",
                        expanded=(i == 1)
                    ):
                        st.markdown(f"**Gap:** {hypo['gap']}")
                        st.markdown("**Proposal:**")
                        st.markdown(hypo['proposal'])
            
            with tab2:
                st.subheader("Identified Research Gaps")
                for i, gap in enumerate(final_state.get('gaps', []), 1):
                    st.markdown(f"{i}. {gap}")
            
            with tab3:
                st.subheader("Multi-Agent Debates")
                
                for i, debate in enumerate(final_state.get('debates', [])[:3], 1):
                    st.markdown(f"### Debate {i}")
                    st.markdown(f"**Gap:** {debate['gap']}")
                    
                    col_pro, col_con = st.columns(2)
                    with col_pro:
                        st.markdown("**✅ Pro Arguments**")
                        st.markdown(debate['pro_arguments'])
                    
                    with col_con:
                        st.markdown("**⚠️ Challenges**")
                        st.markdown(debate['con_arguments'])
                    
                    st.markdown("---")
            
            with tab4:
                st.subheader("Privacy & MCP Protocol Analysis")
                
                col_m1, col_m2, col_m3 = st.columns(3)
                
                with col_m1:
                    st.metric("Privacy Budget (ε)", f"{epsilon}")
                    st.metric("MCP Messages", len(final_state.get('mcp_messages', [])))
                
                with col_m2:
                    st.metric("Agent Actions", len(final_state.get('reasoning_trace', [])))
                    st.metric("Iterations", final_state.get('iteration', 0))
                
                with col_m3:
                    st.metric("DP-Protected Chunks", sum(d['num_chunks'] for d in processed_docs))
                    st.metric("Protocol", "MCP-DP-v1.0")
                
                with st.expander("🔐 MCP Message History"):
                    st.json(final_state.get('mcp_messages', []))
                
                with st.expander("🔍 Reasoning Trace"):
                    st.json(final_state.get('reasoning_trace', []))
            
            st.markdown("---")
            st.header("💾 Download GapForge Report")
            
            report_gen = ReportGenerator()
            
            col_r1, col_r2, col_r3 = st.columns(3)
            
            with col_r1:
                markdown_report = report_gen.generate_markdown_report(final_state)
                st.download_button(
                    label="📄 Download Markdown Report",
                    data=markdown_report,
                    file_name=f"gapforge_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    width='stretch'
                )
            
            with col_r2:
                json_artifact = report_gen.generate_json_artifact(final_state)
                st.download_button(
                    label="📊 Download JSON Artifact",
                    data=json.dumps(json_artifact, indent=2),
                    file_name=f"gapforge_artifact_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    width='stretch'
                )
            
            with col_r3:
                if st.button("🎨 Generate Reasoning Graph", width='stretch'):
                    with st.spinner("Creating visualization..."):
                        try:
                            graph_path = report_gen.generate_reasoning_graph(
                                final_state,
                                output_path="outputs/reasoning_trace"
                            )
                            
                            if os.path.exists(graph_path):
                                st.image(graph_path, caption="Agent Reasoning Trace")
                            else:
                                st.warning(f"Graph file not found: {graph_path}")
                        except Exception as e:
                            st.error(f"Graph generation error: {str(e)}")
            
            st.success("✅ Analysis complete! Download your GapForge Report above.")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
<small>ContextForge v2.0 | Privacy-Preserving Multi-Agent Gap Detector<br>
Powered by CrewAI + Ollama (FREE) + OpenAlex + LangGraph + Differential Privacy<br>
No API keys needed! Run completely locally or with free APIs ✨</small>
</div>
""", unsafe_allow_html=True)
