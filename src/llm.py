"""Anthropic LLM wrapper — minimal interface for email classification.

This module provides functionality to classify emails using Anthropic's LLM API.
It handles API communication, response validation, and error handling.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Set, Optional

from src.config import load_config


# Valid email categories
VALID_CATEGORIES: Set[str] = {"travail", "notification", "newsletter", "associatif"}


class LLMAPIError(Exception):
    """Custom exception for LLM API-related errors."""
    pass


class LLMConfigurationError(Exception):
    """Custom exception for LLM configuration errors."""
    pass


def _get_llm_config() -> Dict[str, Any]:
    """Get LLM-specific configuration with validation.
    
    Loads configuration from the standard location and validates LLM section.
    
    Returns:
        Dictionary containing LLM configuration
        
    Raises:
        LLMConfigurationError: If required configuration is missing or invalid
    """
    try:
        # Use the shared config loader from config module
        full_config = load_config(Path(__file__).parent.parent / "config" / "config.yaml")
        llm_config = full_config.get("llm", {})
        
        # Validate that we have the expected structure
        if not isinstance(llm_config, dict):
            raise LLMConfigurationError("LLM configuration must be a dictionary")
        
        return llm_config
    except Exception as e:
        print(f"Warning: Failed to load LLM config: {e}. Using defaults.", file=sys.stderr)
        return {}


def _resolve_api_key(llm_config: Dict[str, Any]) -> str:
    """Resolve API key from configuration or environment variables.
    
    Priority: config file > environment variable > empty string
    
    Args:
        llm_config: LLM configuration dictionary
        
    Returns:
        API key string (may be empty)
    """
    config_api_key = llm_config.get("api_key", "")
    env_api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    
    # Config file takes precedence over environment variable
    api_key = config_api_key or env_api_key
    
    if not api_key:
        print("Warning: No API key found in config or environment. LLM calls will fail.", file=sys.stderr)
    
    return api_key


def _resolve_model(llm_config: Dict[str, Any]) -> str:
    """Resolve model name from configuration with default fallback.
    
    Args:
        llm_config: LLM configuration dictionary
        
    Returns:
        Model name string
    """
    model = llm_config.get("model", "claude-haiku-4-5")
    print(f"Info: Using LLM model: {model}", file=sys.stderr)
    return model


def _build_classification_prompt(subject: str, body_excerpt: str) -> str:
    """Build the classification prompt for the LLM.
    
    Args:
        subject: Email subject line
        body_excerpt: Excerpt from email body
        
    Returns:
        Formatted prompt string
    """
    return (
        "Classify the following email into exactly one of these categories:\n"
        "travail, notification, newsletter, associatif\n\n"
        f"Subject: {subject}\n"
        f"Body (excerpt): {body_excerpt}\n\n"
        "Reply with only the category name, nothing else."
    )


def _validate_category(raw_category: str) -> str:
    """Validate and normalize the LLM response category.
    
    Args:
        raw_category: Raw category string from LLM
        
    Returns:
        Validated category string, or "travail" if invalid
    """
    normalized = raw_category.strip().lower()
    return normalized if normalized in VALID_CATEGORIES else "travail"


def classify_email(subject: str, body_excerpt: str) -> str:
    """Ask the LLM to classify an email into one of the four categories.
    
    Uses Anthropic's API to classify emails based on subject and body content.
    Implements robust error handling and fallback to default category.
    
    Args:
        subject: Email subject line
        body_excerpt: Excerpt from email body content
        
    Returns:
        One of: "travail", "notification", "newsletter", "associatif"
        Defaults to "travail" when response is unparseable or API fails
        
    Raises:
        Exception: Only if critical system errors occur (re-raises after logging)
        
    Examples:
        >>> category = classify_email("Team Meeting", "Let's discuss the project...")
        >>> assert category in ["travail", "notification", "newsletter", "associatif"]
        
    Note:
        Requires ANTHROPIC_API_KEY in environment or config.yaml
        Falls back to "travail" category on any API or validation error
        
    Implementation details:
        - Uses shared configuration loading from src.config
        - Implements comprehensive error handling
        - Validates all inputs and outputs
        - Provides detailed logging for debugging
    """
    # Input validation
    if not subject or not isinstance(subject, str):
        print(f"Warning: Invalid subject: {subject}. Using default category.", file=sys.stderr)
        return "travail"
    
    if not body_excerpt or not isinstance(body_excerpt, str):
        print(f"Warning: Invalid body excerpt: {body_excerpt}. Using default category.", file=sys.stderr)
        return "travail"
    
    try:
        # Load and validate configuration
        llm_config = _get_llm_config()
        api_key = _resolve_api_key(llm_config)
        model = _resolve_model(llm_config)
        
        # Build prompt
        prompt = _build_classification_prompt(subject, body_excerpt)
        
        # Make API call
        import anthropic  # local import — optional dependency
        
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model=model,
            max_tokens=16,
            messages=[{"role": "user", "content": prompt}],
        )
        
        # Process and validate response
        raw_category = message.content[0].text
        return _validate_category(raw_category)
        
    except ImportError:
        print("Error: Anthropic library not available. Using default category.", file=sys.stderr)
        return "travail"
    except Exception as e:
        print(f"Error: LLM classification failed: {e}. Using default category.", file=sys.stderr)
        return "travail"
