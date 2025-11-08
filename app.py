import streamlit as st
import os
from document_processor import DocumentProcessor
from agents import MultiAgentSystem
from report_generator import ReportGenerator
import json
from datetime import datetime

st.set_page_config(
    page_title="ContextForge - Privacy-Preserving Research Gap Detector",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 ContextForge")
st.markdown("### Privacy-Preserving Multi-Agent Research Gap Detector")
st.markdown("*Powered by MCP Protocol + Differential Privacy*")

st.sidebar.header("⚙️ Configuration")
model_choice = st.sidebar.selectbox(
    "LLM Model",
    ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
    index=0
)

max_iterations = st.sidebar.slider(
    "Agent Iterations",
    min_value=1,
    max_value=5,
    value=3,
    help="Number of evolutionary cycles for hypothesis refinement"
)

epsilon = st.sidebar.slider(
    "Privacy Budget (ε)",
    min_value=0.1,
    max_value=5.0,
    value=1.0,
    step=0.1,
    help="Lower values = more privacy, higher values = more accuracy"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**How it works:**
1. Upload research papers (PDF/DOCX/TXT)
2. System ingests with DP-protected embeddings
3. 4 specialized agents analyze via MCP protocol:
   - **GapDetector**: Finds research gaps
   - **Debater**: Multi-view analysis
   - **HypoGenerator**: Creates hypotheses
   - **Evolver**: Scores & refines
4. Download GapForge Report with MVP proposals
""")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("📄 Upload Research Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, or TXT files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="Upload papers on AI safety, biomedicine, or any research domain"
    )

with col2:
    st.header("🎯 Research Goal")
    research_goal = st.text_area(
        "What gaps are you exploring?",
        value="Find underexplored privacy and safety gaps in AI research",
        height=150,
        help="Optional: Guide the analysis focus"
    )

if uploaded_files:
    st.success(f"✅ Loaded {len(uploaded_files)} document(s)")
    
    if st.button("🚀 Run Multi-Agent Analysis", type="primary", use_container_width=True):
        with st.spinner("🔄 Processing documents with differential privacy..."):
            processor = DocumentProcessor()
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
                    max_iterations=max_iterations
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
                    use_container_width=True
                )
            
            with col_r2:
                json_artifact = report_gen.generate_json_artifact(final_state)
                st.download_button(
                    label="📊 Download JSON Artifact",
                    data=json.dumps(json_artifact, indent=2),
                    file_name=f"gapforge_artifact_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col_r3:
                if st.button("🎨 Generate Reasoning Graph", use_container_width=True):
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

else:
    st.info("👆 Upload research documents to begin privacy-preserving gap analysis")
    
    st.markdown("---")
    st.header("🎓 Example Use Cases")
    
    col_ex1, col_ex2, col_ex3 = st.columns(3)
    
    with col_ex1:
        st.markdown("""
        **AI Safety Research**
        - Find gaps in multilingual jailbreak datasets
        - Privacy-preserving benchmark generation
        - Cross-dialect safety testing
        """)
    
    with col_ex2:
        st.markdown("""
        **Biomedical AI**
        - Drug repurposing hypothesis generation
        - Privacy in clinical trial analysis
        - RNA folding gap detection
        """)
    
    with col_ex3:
        st.markdown("""
        **General Research**
        - Literature gap identification
        - Cross-domain opportunity discovery
        - 24h MVP proposal generation
        """)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
<small>ContextForge v1.0 | Privacy-Preserving Multi-Agent Gap Detector<br>
Powered by LangGraph, OpenAI, Differential Privacy, and Simulated MCP Protocol</small>
</div>
""", unsafe_allow_html=True)
