
from typing import AsyncIterator, Dict, Optional
from nolimitai.config import Config
from nolimitai.core import Router


class NolimitAI:
    """
    NolimitAI is a class that provides an interface to interact with multiple AI services through a unified API. It uses a Router to manage the routing of requests to different services based on a round-robin strategy, allowing for load balancing and failover.
    
    Args: 
        config (Config): An instance of the Config class that contains the configuration for the AI services, including API keys and other parameters.
    Methods:
        set_config: A method to update the configuration of the NolimitAI instance after it has
        been initialized.
        chat: An asynchronous method that takes a prompt and other optional parameters, routes the request to the appropriate AI service, and yields the response in chunks as it is received.
    """
    
    def __init__(self):
        self.config = None
        self.router = None
        
    def set_config(self, temperature: Optional[float] = None, max_tokens: Optional[int] = None, top_p: Optional[float] = None, keys: Dict[str, str] = None) -> None:
        """Set the configuration for NolimitAI. This allows you to update the configuration after initialization."""
        
        config = Config.set_config(
            temperature = temperature,
            max_tokens = max_tokens,
            top_p = top_p,
            keys = keys,
        )
        self.config = config
        self.router = Router(config=self.config)
        
    async def chat(self, prompt: str, model: str, context: Optional[dict] = None, session_id: str = "default", user_id: Optional[str] = None) -> AsyncIterator[str]:
        
        if not self.router:
            raise RuntimeError("NoLimitIA no ha sido configurado. Llama a set_config() primero.")
        
        async for chunk in self.router.route(
            prompt=prompt,
            model=model,
            context=context,
            session_id=session_id,
            user_id=user_id
        ):
            yield chunk  # Yield each token as it arrives