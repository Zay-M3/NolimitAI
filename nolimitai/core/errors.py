"""Utility to extract HTTP status codes from any provider SDK exception.

This module is provider-agnostic. It inspects exception attributes to detect
the HTTP status code regardless of which SDK raised the error, covering:

- Groq, OpenAI, Together, Cohere, Mistral  →  exc.status_code
- Google Generative AI                      →  exc.code
- HuggingFace Hub                           →  exc.response.status_code
"""

from __future__ import annotations

from typing import Optional, Set

_RETRYABLE_STATUS_CODES: Set[int] = {429, 503, 402,502}
_AUTH_STATUS_CODES: Set[int] = {401, 403}


def extract_status_code(exc: Exception) -> Optional[int]:
    """Extract the HTTP status code from any provider SDK exception.

    Returns None when the status code cannot be determined.
    """
    # Groq, OpenAI, Together, Cohere, Mistral — direct .status_code attribute
    status_code = getattr(exc, "status_code", None)
    if isinstance(status_code, int):
        return status_code

    # Google Generative AI — uses .code
    code = getattr(exc, "code", None)
    if isinstance(code, int):
        return code

    # HuggingFace Hub — status code lives inside .response
    response = getattr(exc, "response", None)
    if response is not None:
        resp_status = getattr(response, "status_code", None)
        if isinstance(resp_status, int):
            return resp_status

    return None


def is_retryable(exc: Exception) -> bool:
    """Return True if the exception indicates rate limiting or temporary unavailability (429, 503)."""
    code = extract_status_code(exc)
    return code in _RETRYABLE_STATUS_CODES if code is not None else False


def is_auth_error(exc: Exception) -> bool:
    """Return True if the exception indicates an authentication or permission error (401, 403)."""
    code = extract_status_code(exc)
    return code in _AUTH_STATUS_CODES if code is not None else False
