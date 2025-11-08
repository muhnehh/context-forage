import numpy as np
from diffprivlib.mechanisms import Laplace
from typing import List, Dict, Any
import json

class PrivacyLayer:
    def __init__(self, epsilon: float = 1.0, sensitivity: float = 1.0):
        self.epsilon = epsilon
        self.sensitivity = sensitivity
        self.laplace = Laplace(epsilon=epsilon, sensitivity=sensitivity)
    
    def perturb_embedding(self, embedding: List[float]) -> List[float]:
        embedding_array = np.array(embedding)
        perturbed = np.array([
            self.laplace.randomise(val) for val in embedding_array
        ])
        return perturbed.tolist()
    
    def perturb_embeddings(self, embeddings: List[List[float]]) -> List[List[float]]:
        return [self.perturb_embedding(emb) for emb in embeddings]
    
    def create_mcp_envelope(
        self, 
        context_id: str, 
        data: Any, 
        add_noise: bool = True
    ) -> Dict[str, Any]:
        if add_noise and isinstance(data, (list, np.ndarray)):
            if len(data) > 0 and isinstance(data[0], (int, float)):
                perturbed_data = self.perturb_embedding(list(data) if isinstance(data, np.ndarray) else data)
            else:
                perturbed_data = data
        else:
            perturbed_data = data
        
        envelope = {
            "context_id": context_id,
            "data": perturbed_data,
            "privacy_level": f"epsilon={self.epsilon}",
            "protocol": "MCP-DP-v1.0"
        }
        return envelope
    
    def extract_from_mcp(self, envelope: Dict[str, Any]) -> Any:
        return envelope.get("data")
    
    def add_text_noise(self, text: str, noise_level: float = 0.1) -> str:
        if np.random.random() < noise_level:
            words = text.split()
            if len(words) > 5:
                random_idx = np.random.randint(0, len(words))
                words.insert(random_idx, "[DP-NOISE]")
                return " ".join(words)
        return text
