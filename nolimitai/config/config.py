
from ast import Dict, List
from dataclasses import dataclass, field
from typing import Optional

from pyparsing import Optional


@dataclass(frozen=True)
class Config:
    """Configuration for the nolimit-ai package.
    this class is frozen to prevent modification after creation, ensuring immutability of the configuration.
    
    here we define the API keys for various services that nolimit-ai may interact with. Each key is associated with an environment variable name, allowing for secure and flexible configuration management.
    
    """
    
    # Internal mapping of supported services
    _SUPPORTED_SERVICES: List[str] = field(default_factory=lambda: [
        'groq', 'openrouter', 'together_ai', 'google_generative_ai', 
        'mistral_ai', 'cohere', 'huggingface', 'deepinfra'
    ])
    
    # The actual keys provided by the user
    _vault: Dict[str, str] = field(default_factory=dict)
    
    def from_dict(cls, keys : Dict[str, str]):
        """
        Creates a Config instance from a dictionary.
        Filters only the supported services.
        """
        
        valid_keys = {
            service: key
            for service, key in keys.items()            if service in cls._SUPPORTED_SERVICES
        }
        return cls(_vault=valid_keys)
                
    def get_avalited_service(self) -> List[str]:
        """Returns a list of services that have valid API keys configured."""
        return list(self._vault.keys())
    
    def get_key(self, service: str) -> Optional[str]:
        """Retrieves the API key for a given service."""
        if service not in self._vault:
            raise ValueError(f"Service '{service}' is not configured.")
        return self._vault.get(service)