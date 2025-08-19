# mcp_server/logic.py - Enhanced with three-category wealth system

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
            "examples": ["Startup founders/CEOs", "Corporate executives with equity", "Real estate investors", "Business owners"]
        },
        "partnership_interest": {
            "description": "Partners in professional practices/firms", 
            "examples": ["Law firm partners", "Medical practice owners", "Dentists", "PE/HF principals", "Accounting firm partners"]
        },
        "general_wealth": {
            "description": "Traditional W-2 employees and diversified wealth",
            "examples": ["Engineers", "Teachers", "Managers", "Retirees", "Trust beneficiaries", "Most corporate employees"]
        }
    }

def get_us_session_flow(session_type, user_context):
    """Define conversation flow for US users with three-category system"""
    
    flows = {
        'session1': [
            "PHASE 1: Quick wealth category assessment (concentrated_equity, partnership_interest, or general_wealth)",
            "Ask what they do for work - make quick assessment, don't over-interrogate", 
            "PHASE 2: Family basics (marital status, children) - only after wealth category stored",
            "PHASE 3: Provide category-appropriate recommendations",
            "Store all facts and create actionable next steps"
        ],
        'session2': [
            "Review previously stored wealth category and family facts",
            "Dive deeper into category-specific optimization opportunities",
            "Provide detailed recommendations based on their wealth type",
            "Create implementation timeline",
            "Set follow-up goals"
        ]
    }
    
    return flows.get(session_type, flows['session1'])

def get_us_conversation_flow(session_type):
    """Get conversation flow priorities for US users"""
    
    flows = {
        'session1': [
            "Quick work assessment to determine wealth category",
            "Family basics after wealth category is clear", 
            "Category-specific financial recommendations",
            "Actionable next steps"
        ],
        'session2': [
            "Review stored wealth category and family facts",
            "Analyze category-specific optimization opportunities",
            "Provide detailed implementation plan",
            "Set measurable financial goals"
        ]
    }
    
    return flows.get(session_type, flows['session1'])

def get_us_question_priorities(session_type):
    """Get priority questions for US users with three-category focus"""
    
    questions = {
        'session1': [
            "What do you do for work?",
            "Simple follow-up if needed to categorize wealth type", 
            "Are you married or single? (only after wealth category stored)",
            "Do you have children? (only after wealth category stored)"
        ],
        'session2': [
            "Let's review your wealth category and family situation...",
            "Have you
