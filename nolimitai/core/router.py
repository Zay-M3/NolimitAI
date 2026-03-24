from nolimitai.config.config import Config
from nolimitai.core import RoundRobin
from nolimitai.core.errors import is_retryable, is_auth_error
from nolimitai.memory import CacheMemory
from typing import Dict, List, Optional, AsyncIterator
from nolimitai.adapters import ADAPTERS_FACTORIES

class Router:
    def __init__(self, config: Config):
        self.config = config
        self.cache = CacheMemory()
        self.session_ttl_seconds = 3600
        self.services = self.config.get_available_services()
        self.round_robin = RoundRobin(self.services)
        self.agent_index = 0
        self._last_used_service: Optional[str] = None
        self._last_route_trace: List[str] = []

    def get_last_used_service(self) -> Optional[str]:
        """Returns the provider that successfully handled the latest request."""
        return self._last_used_service

    def get_last_route_trace(self) -> List[str]:
        """Returns providers attempted in the latest route call, in order."""
        return list(self._last_route_trace)

    def get_next_service(self) -> Optional[str]:
        """Returns the next provider that round robin would pick."""
        if self.round_robin.is_empty:
            return None
        return self.round_robin.peek()

    def _messages_cache_key(self, session_id: str, user_id: Optional[str] = None) -> str:
        if user_id:
            return f"user:{user_id}:session:{session_id}:messages"
        return f"session:{session_id}:messages"

    def get_session_messages(self, session_id: str, user_id: Optional[str] = None) -> List[Dict]:
        cache_key = self._messages_cache_key(session_id=session_id, user_id=user_id)
        messages = self.cache.get(cache_key, default=[])
        if not isinstance(messages, list):
            return []
        return messages
        
    async def route(
        self,
        prompt: str,
        model: str,
        context: Optional[dict] = None,
        session_id: str = "default",
        user_id: Optional[str] = None,
    ) -> AsyncIterator[str]:
        """
        This is the master funcion, router, where it wil take a prompt and send to the service, also save the context and to rotate the service using the round robin implementation. this for evit the rate limit of the service, and also to have a better performance.
        
        """

        if self.round_robin.is_empty:
            raise ValueError("No services available to route the task.")
        
        attempts = 0
        max_attempts = len(self.services)
        self._last_route_trace = []
        
        cache_key = self._messages_cache_key(session_id=session_id, user_id=user_id)
        messages = list(self.get_session_messages(session_id=session_id, user_id=user_id))
        
        content_text = prompt if prompt else ""
        
        if context:     
            content_text = f"Context: {context}\n\nUser Question: {prompt}"
            
        message = {"role": "user", "content": str(content_text)}
        
        if context:
            message["context"] = context

        messages.append(message)
        
        
        while(attempts < max_attempts):
            service = self.round_robin.next()
            self._last_route_trace.append(service)
    
            if service not in self.services:
                attempts += 1
                continue
                
            factory = ADAPTERS_FACTORIES.get(service)
            
            if factory is None:
                raise ValueError(f"No adapter found for service '{service}'.")
            
            adapter = factory(
                api_key=self.config.get_key(service),
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p,
            )
            try:
                full_response = ""
                started_streaming = False
                
                async for chunk in adapter.chat(model=model, messages=messages):
                    started_streaming = True
                    self._last_used_service = service
                    full_response += chunk
                    yield chunk  
                messages.append({"role": "assistant", "content": full_response})
                self.cache.set(cache_key, messages, ttl_seconds=self.session_ttl_seconds)
                return
            except Exception as e:
                if started_streaming:
                    raise e
                
                if is_retryable(e) or is_auth_error(e):
                    attempts += 1
                    continue
                raise
            
        raise ValueError("All services failed to process the request after multiple attempts.")
            
            
            
        
        
        

    