from datetime import datetime
from typing import Any, Dict, List
import uuid


def generate_uuid() -> str:
    """
    Generate a UUID string
    """
    return str(uuid.uuid4())


def format_datetime(dt: datetime) -> str:
    """
    Format datetime as ISO string
    """
    return dt.isoformat() if dt else None


def sanitize_input(text: str) -> str:
    """
    Sanitize input text
    """
    if not text:
        return text
    return text.strip()


def merge_dicts(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two dictionaries, with update values overriding base values
    """
    result = base.copy()
    result.update(update)
    return result


def filter_dict(data: Dict[str, Any], allowed_keys: List[str]) -> Dict[str, Any]:
    """
    Filter dictionary to only include allowed keys
    """
    return {k: v for k, v in data.items() if k in allowed_keys}


def dict_to_camel_case(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert dictionary keys from snake_case to camelCase
    """
    result = {}
    for key, value in data.items():
        # Convert snake_case to camelCase
        camel_key = ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(key.split('_')))
        camel_key = camel_key[0].lower() + camel_key[1:] if camel_key else camel_key
        result[camel_key] = value
    return result


def dict_to_snake_case(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert dictionary keys from camelCase to snake_case
    """
    import re
    result = {}
    for key, value in data.items():
        # Convert camelCase to snake_case
        snake_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()
        result[snake_key] = value
    return result