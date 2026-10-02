"""
Acme Corp Internal Knowledge Base Assistant
Module: LLM & Embedding Factory

This module provides a unified interface for initializing chat models and
embeddings engines based on the environment configuration in config.py.

Key Features:
1. 100% Local Inference by Default: Uses ChatOllama and FastEmbed.
2. Vendor Agility: Switch between local Ollama, OpenAI, or Anthropic simply
   by changing LLM_PROVIDER in .env without modifying application logic.
3. Content Normalization: Standardizes model outputs across diverse API providers.
"""

from typing import Any
from . import config


def get_llm(temperature: float = 0.0) -> Any:
    """
    Return an initialized Chat Model instance.
    
    Args:
        temperature: Sampling temperature (0.0 = deterministic/greedy, 1.0 = creative).
                     In enterprise policy and tool-calling agents, 0.0 is strongly
                     recommended to minimize variance and hallucinations.
    """
    provider = config.LLM_PROVIDER

    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=config.LLM_MODEL,
            temperature=temperature,
            base_url=config.OLLAMA_BASE_URL,
        )

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=config.LLM_MODEL or "gpt-4o-mini",
            temperature=temperature,
        )

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=config.LLM_MODEL or "claude-3-haiku-20240307",
            temperature=temperature,
        )

    raise ValueError(
        f"Unsupported LLM_PROVIDER '{provider}'. Supported options: 'ollama', 'openai', 'anthropic'."
    )


def get_embeddings() -> Any:
    """
    Return an initialized Embeddings Engine instance.
    
    Defaults to FastEmbed (runs quantized BAAI/bge-small-en-v1.5 locally on CPU).
    Zero API cost, zero external network dependency.
    """
    provider = config.EMBEDDINGS_PROVIDER

    if provider == "local":
        # FastEmbed uses ONNX runtime on CPU; no GPU or PyTorch install needed
        from langchain_community.embeddings import FastEmbedEmbeddings
        return FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

    if provider == "ollama":
        from langchain_ollama import OllamaEmbeddings
        return OllamaEmbeddings(
            model="nomic-embed-text",
            base_url=config.OLLAMA_BASE_URL,
        )

    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model="text-embedding-3-small")

    raise ValueError(
        f"Unsupported EMBEDDINGS_PROVIDER '{provider}'. Supported options: 'local', 'ollama', 'openai'."
    )


def text_of(message: Any) -> str:
    """
    Extract raw text content from a LangChain message object.
    
    Different providers format responses differently:
    - Some return a plain string in `message.content`
    - Some (like Anthropic or multimodal models) return a list of content blocks
    
    This function normalizes all responses into a single UTF-8 string.
    """
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and "text" in block:
                parts.append(block["text"])
        return "".join(parts)
    return str(content)
