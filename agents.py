from typing import Dict, Any, List, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from mcp_simulator import MCPSimulator
import json

class AgentState(TypedDict):
    documents: List[Dict[str, Any]]
    gaps: List[str]
    debates: List[Dict[str, Any]]
    hypotheses: List[Dict[str, Any]]
    final_hypotheses: List[Dict[str, Any]]
    iteration: int
    max_iterations: int
    mcp_messages: List[Dict[str, Any]]
    reasoning_trace: List[Dict[str, Any]]

class MultiAgentSystem:
    def __init__(self, model_name: str = "gpt-4o-mini", max_iterations: int = 3, epsilon: float = 1.0):
        self.llm = ChatOpenAI(model=model_name, temperature=0.7)
        self.mcp = MCPSimulator(epsilon=epsilon)
        self.max_iterations = max_iterations
        self.epsilon = epsilon
        self.graph = self._build_graph()
    
    def _gap_detector(self, state: AgentState) -> AgentState:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are GapDetector, an expert at identifying research gaps and limitations.
            Analyze the provided documents and identify:
            1. Underexplored areas or missing perspectives
            2. Technical limitations or privacy concerns
            3. Methodological gaps or untested scenarios
            4. Cross-domain opportunities (e.g., privacy in biomedical AI, multilingual safety)
            
            Focus on actionable gaps that could lead to 24-hour buildable MVPs."""),
            ("user", "Documents:\n{documents}\n\nIdentify 3-5 key research gaps:")
        ])
        
        docs_text = "\n\n".join([
            f"Document: {doc.get('file_name', 'Unknown')}\n{doc.get('full_text', '')[:2000]}..."
            for doc in state["documents"]
        ])
        
        response = self.llm.invoke(prompt.format_messages(documents=docs_text))
        gaps_text = str(response.content)
        
        gaps = [line.strip() for line in gaps_text.split('\n') if line.strip() and not line.startswith('#')]
        gaps = [g for g in gaps if len(g) > 20][:5]
        
        mcp_message = self.mcp.share_context(
            from_agent="GapDetector",
            to_agent="Debater",
            data={"gaps": gaps, "analysis": gaps_text}
        )
        
        state["gaps"] = gaps
        state["mcp_messages"].append(mcp_message)
        state["reasoning_trace"].append({
            "agent": "GapDetector",
            "action": "identified_gaps",
            "output": gaps,
            "iteration": state["iteration"]
        })
        
        return state
    
    def _debater(self, state: AgentState) -> AgentState:
        debates = []
        
        for gap in state["gaps"][:3]:
            pro_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a research advocate arguing WHY this gap is important and worth pursuing."),
                ("user", "Gap: {gap}\n\nProvide 3-4 strong arguments for pursuing this research gap:")
            ])
            
            con_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a critical reviewer identifying challenges and limitations."),
                ("user", "Gap: {gap}\n\nProvide 3-4 challenges or reasons to be cautious about this gap:")
            ])
            
            pro_response = self.llm.invoke(pro_prompt.format_messages(gap=gap))
            con_response = self.llm.invoke(con_prompt.format_messages(gap=gap))
            
            debate = {
                "gap": gap,
                "pro_arguments": pro_response.content,
                "con_arguments": con_response.content,
                "iteration": state["iteration"]
            }
            debates.append(debate)
        
        mcp_message = self.mcp.share_context(
            from_agent="Debater",
            to_agent="HypoGenerator",
            data={"debates": debates}
        )
        
        state["debates"].extend(debates)
        state["mcp_messages"].append(mcp_message)
        state["reasoning_trace"].append({
            "agent": "Debater",
            "action": "conducted_debates",
            "output": f"Debated {len(debates)} gaps",
            "iteration": state["iteration"]
        })
        
        return state
    
    def _hypo_generator(self, state: AgentState) -> AgentState:
        hypotheses = []
        
        recent_debates = [d for d in state["debates"] if d["iteration"] == state["iteration"]]
        
        for debate in recent_debates:
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are HypoGenerator, creating novel research hypotheses and 24-hour MVP proposals.
                Based on the gap and debate, propose:
                1. A specific, testable hypothesis
                2. A concrete 24-hour buildable MVP (dataset, tool, or benchmark)
                3. Technical approach and expected impact
                
                Focus on privacy-preserving, ethical AI applications."""),
                ("user", """Gap: {gap}
                
Pro Arguments:
{pro_args}

Critical Challenges:
{con_args}

Generate a hypothesis and 24h MVP proposal:""")
            ])
            
            response = self.llm.invoke(prompt.format_messages(
                gap=debate["gap"],
                pro_args=debate["pro_arguments"],
                con_args=debate["con_arguments"]
            ))
            
            hypothesis = {
                "gap": debate["gap"],
                "proposal": response.content,
                "iteration": state["iteration"],
                "score": 0.0
            }
            hypotheses.append(hypothesis)
        
        mcp_message = self.mcp.share_context(
            from_agent="HypoGenerator",
            to_agent="Evolver",
            data={"hypotheses": hypotheses}
        )
        
        state["hypotheses"].extend(hypotheses)
        state["mcp_messages"].append(mcp_message)
        state["reasoning_trace"].append({
            "agent": "HypoGenerator",
            "action": "generated_hypotheses",
            "output": f"Generated {len(hypotheses)} hypotheses",
            "iteration": state["iteration"]
        })
        
        return state
    
    def _evolver(self, state: AgentState) -> AgentState:
        recent_hypotheses = [h for h in state["hypotheses"] if h["iteration"] == state["iteration"]]
        
        for hypo in recent_hypotheses:
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are Evolver, scoring and improving research hypotheses.
                Score from 0-10 based on:
                - Novelty (0-3): Is this underexplored?
                - Feasibility (0-3): Can this be built in 24 hours?
                - Impact (0-2): Does this address ethics/privacy/safety?
                - Privacy Integration (0-2): Does it use DP or MCP concepts?
                
                Provide ONLY a number between 0-10."""),
                ("user", "Hypothesis:\n{proposal}\n\nScore (0-10):")
            ])
            
            response = self.llm.invoke(prompt.format_messages(proposal=hypo["proposal"]))
            
            try:
                score = float(str(response.content).strip().split()[0])
                score = max(0.0, min(10.0, score))
            except:
                score = 5.0
            
            hypo["score"] = score
        
        state["hypotheses"] = sorted(
            state["hypotheses"], 
            key=lambda x: x.get("score", 0), 
            reverse=True
        )
        
        top_hypotheses = state["hypotheses"][:3]
        
        state["iteration"] += 1
        
        mcp_message = self.mcp.share_context(
            from_agent="Evolver",
            to_agent="Coordinator",
            data={"top_hypotheses": top_hypotheses, "iteration": state["iteration"]}
        )
        
        state["mcp_messages"].append(mcp_message)
        state["reasoning_trace"].append({
            "agent": "Evolver",
            "action": "scored_and_evolved",
            "output": f"Top score: {top_hypotheses[0]['score'] if top_hypotheses else 0}",
            "iteration": state["iteration"] - 1
        })
        
        return state
    
    def _should_continue(self, state: AgentState) -> str:
        if state["iteration"] >= state["max_iterations"]:
            return "finalize"
        return "continue"
    
    def _finalize(self, state: AgentState) -> AgentState:
        state["final_hypotheses"] = state["hypotheses"][:5]
        
        state["reasoning_trace"].append({
            "agent": "Coordinator",
            "action": "finalized",
            "output": f"Selected top {len(state['final_hypotheses'])} hypotheses",
            "iteration": state["iteration"]
        })
        
        return state
    
    def _build_graph(self):
        workflow = StateGraph(AgentState)
        
        workflow.add_node("gap_detector", self._gap_detector)
        workflow.add_node("debater", self._debater)
        workflow.add_node("hypo_generator", self._hypo_generator)
        workflow.add_node("evolver", self._evolver)
        workflow.add_node("finalize", self._finalize)
        
        workflow.set_entry_point("gap_detector")
        
        workflow.add_edge("gap_detector", "debater")
        workflow.add_edge("debater", "hypo_generator")
        workflow.add_edge("hypo_generator", "evolver")
        
        workflow.add_conditional_edges(
            "evolver",
            self._should_continue,
            {
                "continue": "gap_detector",
                "finalize": "finalize"
            }
        )
        
        workflow.add_edge("finalize", END)
        
        return workflow.compile()
    
    def run(self, documents: List[Dict[str, Any]]) -> AgentState:
        initial_state: AgentState = {
            "documents": documents,
            "gaps": [],
            "debates": [],
            "hypotheses": [],
            "final_hypotheses": [],
            "iteration": 0,
            "max_iterations": self.max_iterations,
            "mcp_messages": [],
            "reasoning_trace": []
        }
        
        final_state = self.graph.invoke(initial_state)
        return final_state
