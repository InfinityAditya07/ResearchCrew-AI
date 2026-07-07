"""Strip CrewAI/LiteLLM message fields that Groq and similar providers reject."""

from __future__ import annotations

from typing import Any

import litellm

UNSUPPORTED_MESSAGE_KEYS = frozenset(
    {
        "cache_breakpoint",
        "is_litellm",
        "provider_specific_fields",
    }
)

_original_completion = litellm.completion
_original_acompletion = litellm.acompletion


def _strip_unsupported_message_keys(messages: list[Any]) -> list[Any]:
    cleaned: list[Any] = []
    for message in messages:
        if not isinstance(message, dict):
            cleaned.append(message)
            continue
        cleaned.append(
            {
                key: value
                for key, value in message.items()
                if key not in UNSUPPORTED_MESSAGE_KEYS
            }
        )
    return cleaned


def _prepare_kwargs(kwargs: dict[str, Any]) -> dict[str, Any]:
    messages = kwargs.get("messages")
    if not messages:
        return kwargs
    return {**kwargs, "messages": _strip_unsupported_message_keys(messages)}


def _patched_completion(*args: Any, **kwargs: Any) -> Any:
    return _original_completion(*args, **_prepare_kwargs(kwargs))


async def _patched_acompletion(*args: Any, **kwargs: Any) -> Any:
    return await _original_acompletion(*args, **_prepare_kwargs(kwargs))


def apply_litellm_patch() -> None:
    if getattr(litellm.completion, "_researchcrew_patched", False):
        return
    litellm.completion = _patched_completion
    litellm.acompletion = _patched_acompletion
    litellm.completion._researchcrew_patched = True
