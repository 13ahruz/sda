"""
Utility functions for multilingual content handling
"""
from typing import Any, Dict, Optional

# Supported languages
SUPPORTED_LANGUAGES = ['en', 'az', 'ru']
DEFAULT_LANGUAGE = 'en'

def get_localized_field(obj: Any, field_base: str, language: str = DEFAULT_LANGUAGE, fallback: bool = True) -> Optional[str]:
    """
    Get localized field value from a model object.
    
    Args:
        obj: The model object
        field_base: Base field name (e.g., 'title', 'description')
        language: Language code ('en', 'az', 'ru')
        fallback: Whether to fallback to other languages if requested language is not available
    
    Returns:
        The localized field value or None if not found
    """
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE
    
    # Try to get the requested language
    field_name = f"{field_base}_{language}"
    value = getattr(obj, field_name, None)
    
    if value:
        return value
    
    if not fallback:
        return None
    
    # Fallback strategy: try other languages in order of preference
    fallback_languages = [DEFAULT_LANGUAGE] + [lang for lang in SUPPORTED_LANGUAGES if lang != language and lang != DEFAULT_LANGUAGE]
    
    for fallback_lang in fallback_languages:
        if fallback_lang == language:  # Skip if already tried
            continue
            
        fallback_field = f"{field_base}_{fallback_lang}"
        fallback_value = getattr(obj, fallback_field, None)
        if fallback_value:
            return fallback_value
    
    # Final fallback: try legacy field without language suffix
    legacy_value = getattr(obj, field_base, None)
    return legacy_value

def get_multilingual_fields(obj: Any, field_bases: list, language: str = DEFAULT_LANGUAGE) -> Dict[str, Any]:
    """
    Get multiple localized fields from a model object.
    
    Args:
        obj: The model object
        field_bases: List of base field names
        language: Language code
    
    Returns:
        Dictionary with localized field values
    """
    result = {}
    for field_base in field_bases:
        result[field_base] = get_localized_field(obj, field_base, language)
    return result

def validate_language(language: str) -> str:
    """
    Validate and normalize language code.
    
    Args:
        language: Language code to validate
    
    Returns:
        Validated language code or default language
    """
    if language and language.lower() in SUPPORTED_LANGUAGES:
        return language.lower()
    return DEFAULT_LANGUAGE

def get_all_language_versions(obj: Any, field_base: str) -> Dict[str, Optional[str]]:
    """
    Get all language versions of a field.
    
    Args:
        obj: The model object
        field_base: Base field name
    
    Returns:
        Dictionary with all language versions
    """
    result = {}
    for lang in SUPPORTED_LANGUAGES:
        field_name = f"{field_base}_{lang}"
        result[lang] = getattr(obj, field_name, None)
    
    # Also include legacy field if exists
    legacy_value = getattr(obj, field_base, None)
    if legacy_value and not any(result.values()):
        result[DEFAULT_LANGUAGE] = legacy_value
    
    return result

def set_multilingual_field(obj: Any, field_base: str, values: Dict[str, str]) -> None:
    """
    Set multilingual field values on a model object.
    
    Args:
        obj: The model object
        field_base: Base field name
        values: Dictionary with language codes as keys and values as strings
    """
    for lang, value in values.items():
        if lang in SUPPORTED_LANGUAGES:
            field_name = f"{field_base}_{lang}"
            if hasattr(obj, field_name):
                setattr(obj, field_name, value)

def prepare_multilingual_response(obj: Any, field_bases: list, language: str = DEFAULT_LANGUAGE) -> Dict[str, Any]:
    """
    Prepare a response object with localized fields.
    
    Args:
        obj: The model object
        field_bases: List of base field names to include
        language: Language code
    
    Returns:
        Dictionary with localized fields and their values
    """
    response = {}
    
    # Add localized fields
    for field_base in field_bases:
        response[field_base] = get_localized_field(obj, field_base, language)
    
    # Add non-localized fields
    non_localized_fields = ['id', 'slug', 'created_at', 'updated_at', 'order', 
                           'year', 'client', 'tag', 'photo_url', 'image_url', 
                           'cover_photo_url', 'icon_url', 'category', 'author', 
                           'read_time', 'tags', 'property_sector_id']
    
    for field in non_localized_fields:
        if hasattr(obj, field):
            value = getattr(obj, field)
            if value is not None:
                response[field] = value
    
    return response