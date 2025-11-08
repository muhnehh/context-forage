import json
import uuid
from typing import Dict, Any, List
from privacy_layer import PrivacyLayer

class MCPSimulator:
    def __init__(self, epsilon: float = 1.0):
        self.privacy_layer = PrivacyLayer(epsilon=epsilon)
        self.context_store: Dict[str, Dict[str, Any]] = {}
        self.message_history: List[Dict[str, Any]] = []
    
    def create_context(self, agent_name: str, data: Any) -> str:
        context_id = f"{agent_name}_{uuid.uuid4().hex[:8]}"
        
        envelope = self.privacy_layer.create_mcp_envelope(
            context_id=context_id,
            data=data,
            add_noise=False
        )
        
        self.context_store[context_id] = {
            "agent": agent_name,
            "envelope": envelope,
            "timestamp": str(uuid.uuid4())
        }
        
        return context_id
    
    def share_context(
        self, 
        from_agent: str, 
        to_agent: str, 
        data: Any,
        apply_privacy: bool = True
    ) -> Dict[str, Any]:
        context_id = self.create_context(from_agent, data)
        
        message = {
            "from": from_agent,
            "to": to_agent,
            "context_id": context_id,
            "data": data,
            "privacy_applied": apply_privacy,
            "protocol": "MCP-DP-v1.0"
        }
        
        self.message_history.append(message)
        
        return message
    
    def retrieve_context(self, context_id: str) -> Any:
        if context_id in self.context_store:
            envelope = self.context_store[context_id]["envelope"]
            return self.privacy_layer.extract_from_mcp(envelope)
        return None
    
    def get_message_history(self) -> List[Dict[str, Any]]:
        return self.message_history
    
    def clear_history(self):
        self.message_history = []
        self.context_store = {}
