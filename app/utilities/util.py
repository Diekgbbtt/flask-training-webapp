from typing import Any, Optional

from app import session
from jsonschema import validate, ValidationError

def is_client_authn(**kwargs: dict) -> bool :
    return 'username' in session

# JSON Schema for validating objects with two string attributes
USER_SCHEMA = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "password": {
            "type": "string",
            "minLength": 6
        }
    },
    "required": ["username", "password"],
    "additionalProperties": False
}

def validate_user_data(data: dict, schema : Optional[dict]) -> tuple[bool, str]:
    """
    Validate user data against JSON schema.

    Args:
        data: Dictionary containing username and password

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        validate(instance=data, schema=USER_SCHEMA)
        return True, ""
    except ValidationError as e:
        return False, str(e.message)
    except Exception as e:
        return False, f"Validation error: {str(e)}"

