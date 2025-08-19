import json
import os

def get_prompt_instructions(country, language, session_type, user_context):
    """
    Get conversation instructions for US users with three-category wealth system.
    Language/cultural handling is done in Core LLM, this focuses on conversation flow.
    """
    
    # For MVP: Only supporting US
    if country.upper() != 'US':
        return get_default_instructions()
    
    # Build prompt file path - simplified naming (no language since Core LLM handles that)
    prompt_path = os.path.join('mcp_server', 'prompts', f'us_{session_type.lower()}.txt')

    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            instructions = f.read()
    except FileNotFoundError:
        return get_default_instructions()

    # Get US financial context
    financial_context = get_country_financial_context('US')
    
    # Build session-specific flow for US users
    session_flow = get_us_session_flow(session_type, user_context)
    
    # Return structured instructions for US with three-category system
    return {
        "instructions": instructions,
        "financial_context": financial_context,
        "session_flow": session_flow,
        "country": "US",
        "session_type": session_type,
        "conversation_flow": get_us_conversation_flow(session_type),
        "question_priorities": get_us_question_priorities(session_type),
        "tools_to_use": get_us_recommended_tools(session_type),
        "wealth_categories": get_wealth_categories()
    }

def get_wealth_categories():
    """Define the three wealth categories for internal LLM use"""
    return {
        "concentrated_equity": {
            "description": "Ownership in corporations/assets",
            "examples": ["Startup founders/CEOs", "Corporate executives with equity", "Real estate investors", "Business owners"],
            "typical_concerns": ["Diversification", "Liquidity planning", "Tax optimization", "Exit strategies"]
        },
        "partnership_interest": {
            "description": "Partners in professional practices/firms", 
            "examples": ["Law firm partners", "Medical practice owners", "Dentists", "PE/HF principals", "Accounting firm partners"],
            "typical_concerns": ["Distribution planning", "Succession planning", "Tax optimization", "Practice valuation"]
        },
        "general_wealth": {
            "description": "Traditional W-2 employees and diversified wealth",
            "examples": ["Engineers", "Teachers", "Managers", "Retirees", "Trust beneficiaries", "Most corporate employees"],
            "typical_concerns": ["401k optimization", "Emergency funds", "Tax efficiency", "Retirement planning"]
        }
    }

def get_us_session_flow(session_type, user_context):
    """Define conversation flow for US users with three-category system"""
    
    flows = {
        'session1': [
            "PHASE 1: Alter-ego introduction and rapport building",
            "PHASE 2: Source of wealth discovery and internal categorization",
            "PHASE 3: Family structure discovery (only after wealth category is determined)", 
            "PHASE 4: Wealth-category-appropriate follow-up questions",
            "PHASE 5: Summarize understanding and set foundation for future conversations"
        ],
        'session2': [
            "Review stored alter-ego relationship and wealth category",
            "Dive deeper into category-specific financial areas",
            "Provide personalized insights based on their wealth type",
            "Build on previous conversation and stored facts",
            "Continue developing the alter-ego relationship"
        ]
    }
    
    return flows.get(session_type, flows['session1'])

def get_us_conversation_flow(session_type):
    """Get conversation flow priorities for US users"""
    
    flows = {
        'session1': [
            "Required alter-ego introduction explaining Quin's role",
            "Natural source of wealth discovery through work conversation",
            "Internal wealth categorization (user doesn't see categories)", 
            "Family basics after wealth category is clear",
            "Category-appropriate follow-up questions",
            "Relationship summary and foundation setting"
        ],
        'session2': [
            "Acknowledge previous alter-ego relationship",
            "Review stored wealth category and family facts",
            "Analyze category-specific opportunities and concerns",
            "Provide personalized insights as their financial alter-ego",
            "Deepen the ongoing relationship"
        ]
    }
    
    return flows.get(session_type, flows['session1'])

def get_us_question_priorities(session_type):
    """Get priority questions for US users with three-category focus"""
    
    questions = {
        'session1': [
            "Required opening: Explain alter-ego concept with exact script",
            "What do you do for work? (for wealth categorization)",
            "Simple follow-up if needed to categorize wealth type", 
            "Are you married or single? (only after wealth category stored)",
            "Do you have children? (only after wealth category stored)",
            "Wealth-category-appropriate follow-up questions"
        ],
        'session2': [
            "Acknowledge the alter-ego relationship from session 1",
            "Review wealth category and family situation from stored facts",
            "What's changed since we last talked?",
            "What financial area feels most important to focus on?",
            "Category-specific deeper questions"
        ]
    }
    
    return questions.get(session_type, questions['session1'])

def get_us_recommended_tools(session_type):
    """Get recommended tools for US conversations"""
    
    tools = {
        'session1': ['store_user_fact', 'getSavingsRecommendation', 'getInstitutions'],
        'session2': ['store_user_fact', 'getSavingsRecommendation', 'getInstitutions']
    }
    
    return tools.get(session_type, tools['session1'])

def get_available_languages(country):
    """Get available languages - US supports English and Spanish"""
    languages = {
        'US': ['en', 'es']
    }
    return languages.get(country.upper(), ['en'])

def get_country_financial_context(country):
    """Get financial context for US"""
    
    if country.upper() != 'US':
        return get_default_context()
    
    context_path = os.path.join('mcp_server', 'context', 'us_context.json')
    
    try:
        with open(context_path, 'r', encoding='utf-8') as f:
            context = json.load(f)
        
        # Enhance context with wealth category information
        context['wealth_system'] = {
            "categories": ["concentrated_equity", "partnership_interest", "general_wealth"],
            "approach": "Quick assessment through natural work conversation",
            "accuracy_target": "85-90% - user can correct if needed"
        }
        
        return context
        
    except FileNotFoundError:
        return get_default_context()

def get_default_context():
    """Fallback context with wealth category system"""
    return {
        "financial_systems": {
            "insurance": "FDIC insurance up to $250k",
            "retirement_accounts": ["401k", "IRA", "Roth IRA"],
            "taxes": {
                "state": "Varies by state", 
                "federal": "Federal tax brackets apply"
            }
        },
        "conversation_approach": {
            "style": "Alter-ego relationship - AI version of user with financial expertise",
            "privacy": "Ask for approximate numbers only",
            "relationship": "Learning to become their personalized financial alter-ego"
        },
        "wealth_system": {
            "categories": ["concentrated_equity", "partnership_interest", "general_wealth"],
            "approach": "Quick assessment through natural work conversation", 
            "accuracy_target": "85-90% - user can correct if needed"
        }
    }

def get_default_instructions():
    """Fallback instructions with alter-ego approach"""
    return {
        "instructions": "You are Quin, learning to become this user's financial alter-ego. Use the three-category wealth system to understand their situation through natural conversation.",
        "financial_context": get_default_context(),
        "session_flow": ["Alter-ego introduction", "Wealth categorization", "Family basics", "Category-appropriate questions"],
        "country": "US",
        "session_type": "session1",
        "conversation_flow": ["Explain alter-ego concept", "What do you do for work?", "Family situation", "Build relationship"],
        "question_priorities": ["Alter-ego intro", "Work/wealth discovery", "Family", "Relationship building"],
        "tools_to_use": ["store_user_fact", "getSavingsRecommendation"],
        "wealth_categories": get_wealth_categories()
    }
