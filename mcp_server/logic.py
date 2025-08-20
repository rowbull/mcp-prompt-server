import json
import os

def get_prompt_instructions(country, language, session_type, user_context):
    """
    Get conversation instructions for US users with clean onboarding approach.
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
            "description": "Wealth tied to restricted/illiquid assets >30% of net worth",
            "personas": ["startup_founder", "corporate_executive", "business_owner", "direct_investor"],
            "key_test": "Cannot easily diversify due to restrictions + >30% concentration"
        },
        "partnership_interest": {
            "description": "Partners in professional practices/firms with profit sharing", 
            "personas": ["professional_services", "financial_partnership", "large_professional"],
            "key_test": "Ownership stake + profit sharing in partnership structure"
        },
        "general_wealth": {
            "description": "Traditional employees and diversified wealth builders",
            "personas": ["w2_employee", "retiree", "trust_beneficiary", "recent_windfall"],
            "key_test": "Standard employment or diversified assets (default category)"
        }
    }

def get_us_session_flow(session_type, user_context):
    """Define conversation flow for US users - clean onboarding approach"""
    
    flows = {
        'session1': [
            "PHASE 1: Natural introduction - Quin getting to know the user",
            "PHASE 2: Source of wealth discovery (category + persona identification)",
            "PHASE 3: Basic family structure (marital status + children)", 
            "PHASE 4: Profile complete - route to specialized conversation"
        ],
        'session2': [
            "Review stored profile information",
            "Provide specialized guidance based on wealth category and persona",
            "Build on previous conversations"
        ]
    }
    
    return flows.get(session_type, flows['session1'])

def get_us_conversation_flow(session_type):
    """Get conversation flow priorities for US users"""
    
    flows = {
        'session1': [
            "Open with required introduction script",
            "Ask about work/income source naturally",
            "Listen for category signals - assume General Wealth unless proven otherwise", 
            "Clarify only if concentration signals detected",
            "Store wealth category + persona when determined",
            "Ask about family structure (married/single + children)",
            "Complete profile and transition to specialized conversation"
        ],
        'session2': [
            "Acknowledge existing relationship",
            "Reference stored profile data",
            "Provide category-specific insights and guidance"
        ]
    }
    
    return flows.get(session_type, flows['session1'])

def get_us_question_priorities(session_type):
    """Get priority questions for US users - onboarding focused"""
    
    questions = {
        'session1': [
            "Required opening: Use exact introduction script from prompt",
            "What do you do for a living? (natural work conversation)",
            "Clarification if needed: wealth concentration or partnership status", 
            "Are you married or single? (only after SOW stored)",
            "Do you have children? (only after SOW stored)",
            "Profile complete - no additional questions in Session 1"
        ],
        'session2': [
            "Reference profile: wealth category, persona, family status",
            "What financial topics are most important to you?",
            "Category-specific guidance and insights"
        ]
    }
    
    return questions.get(session_type, questions['session1'])

def get_us_recommended_tools(session_type):
    """Get recommended tools for US conversations"""
    
    tools = {
        'session1': ['store_user_fact'],  # Only profile storage for onboarding
        'session2': ['store_user_fact', 'getSavingsRecommendation', 'getInstitutions']  # Full tools for guidance
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
            "approach": "Assume General Wealth, prove out if concentration signals detected",
            "threshold": "30% concentration + liquidity restrictions for concentrated equity"
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
            "style": "Natural conversation to learn about the user",
            "privacy": "Ask for approximate numbers only",
            "purpose": "Collect basic profile to enable personalized guidance"
        },
        "wealth_system": {
            "categories": ["concentrated_equity", "partnership_interest", "general_wealth"],
            "approach": "Assume General Wealth, prove out if concentration signals detected", 
            "threshold": "30% concentration + liquidity restrictions for concentrated equity"
        }
    }

def get_default_instructions():
    """Fallback instructions with clean onboarding approach"""
    return {
        "instructions": "You are Quin. Have a natural conversation to learn about this user's basic profile so you can provide personalized financial guidance.",
        "financial_context": get_default_context(),
        "session_flow": ["Introduction", "Work/wealth discovery", "Family basics", "Profile complete"],
        "country": "US",
        "session_type": "session1",
        "conversation_flow": ["Natural introduction", "What do you do for work?", "Family situation", "Complete profile"],
        "question_priorities": ["Opening script", "Work conversation", "Family questions", "Completion"],
        "tools_to_use": ["store_user_fact"],
        "wealth_categories": get_wealth_categories()
    }
