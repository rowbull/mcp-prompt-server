import json
import os

def get_prompt_instructions(country, language, session_type, user_context):
    # This is a simplified implementation. In a real-world scenario,
    # you would have a more robust way of mapping these parameters to a prompt.
    prompt_path = os.path.join('mcp_server', 'prompts', f'{country.lower()}_{language.lower()}_{session_type.lower()}.txt')

    try:
        with open(prompt_path, 'r') as f:
            instructions = f.read()
    except FileNotFoundError:
        return {"error": "Prompt not found for the given parameters"}

    financial_context = get_country_financial_context(country)

    language_directive = ""
    if language.lower() == 'es':
        language_directive = "Conduct this conversation in Spanish"

    # In a real application, the session flow and cultural approach would be more dynamic
    session_flow = "Session 1 discovery questions and patterns..."
    cultural_approach = "Professional but warm American style"

    return {
        "instructions": instructions,
        "language_directive": language_directive,
        "financial_context": financial_context,
        "session_flow": session_flow,
        "cultural_approach": cultural_approach
    }

def get_available_languages(country):
    # This would be loaded from a config file or database in a real app
    languages = {
        'US': ['en', 'es']
    }
    return languages.get(country, [])

def get_country_financial_context(country):
    context_path = os.path.join('mcp_server', 'context', f'{country.lower()}_context.json')
    try:
        with open(context_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "Financial context not found for the given country"}
