import json
import os

def get_prompt_instructions(country, language, session_type, user_context):
    """
    Get conversation instructions for the specified country and session.
    """
    
    # For MVP: Only supporting US
    if country.upper() != 'US':
        return get_default_instructions()
    
    # Build prompt file path 
    prompt_path = os.path.join('mcp_server', 'prompts', f'us_{session_type.lower()}.txt')

    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            instructions = f.read()
    except FileNotFoundError:
        return get_default_instructions()

    # Get US financial context
    financial_context = get_country_financial_context('US')
    
    # Return clean configuration - prompt handles all conversation logic
    return {
        "instructions": instructions,
        "financial_context": financial_context,
        "country": "US",
        "session_type": session_type,
        "tools_to_use": get_session_tools(session_type)
    }

def get_session_tools(session_type):
    """Get tools available for this session type"""
    
    tools = {
        'session1': ['store_user_fact'],  # Only profile storage for onboarding
        'session2': ['store_user_fact', 'getSavingsRecommendation', 'getInstitutions']  # Full tools for guidance
    }
    
    return tools.get(session_type.lower(), ['store_user_fact'])

def get_available_languages(country):
    """Get available languages for a country"""
    
    languages = {
        'US': ['en', 'es']
    }
    return languages.get(country.upper(), ['en'])

def get_country_financial_context(country):
    """Get financial context for the specified country"""
    
    if country.upper() != 'US':
        return get_default_financial_context()
    
    context_path = os.path.join('mcp_server', 'context', 'us_context.json')
    
    try:
        with open(context_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return get_default_financial_context()

def get_default_financial_context():
    """Default financial context when country-specific not available"""
    
    return {
        "financial_systems": {
            "insurance": "FDIC insurance up to $250k",
            "retirement_accounts": ["401k", "IRA", "Roth IRA"],
            "taxes": {
                "state": "Varies by state", 
                "federal": "Federal tax brackets apply"
            },
            "estate_planning": "Thresholds vary by state"
        },
        "conversation_approach": {
            "style": "Direct, professional but friendly",
            "money_discussion": "Comfortable discussing money openly"
        }
    }

def get_default_instructions():
    """Fallback instructions when prompt file not found"""
    
    return {
        "instructions": "You are Quin. Have a natural conversation to learn about this user's basic profile so you can provide personalized financial guidance.",
        "financial_context": get_default_financial_context(),
        "country": "US",
        "session_type": "session1",
        "tools_to_use": ["store_user_fact"]
    }
