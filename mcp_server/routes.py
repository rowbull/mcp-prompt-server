import json
from flask import Blueprint, jsonify, request
from mcp_server.logic import get_prompt_instructions, get_available_languages, get_country_financial_context

mcp_bp = Blueprint('mcp', __name__)

@mcp_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@mcp_bp.route('/mcp/getPromptInstructions', methods=['POST'])
def prompt_instructions():
    data = request.get_json()
    country = data.get('country')
    language = data.get('language')
    session_type = data.get('sessionType')
    user_context = data.get('userContext')

    if not all([country, language, session_type]):
        return jsonify({"error": "Missing required parameters"}), 400

    instructions = get_prompt_instructions(country, language, session_type, user_context)
    return jsonify(instructions)

@mcp_bp.route('/test/prompt', methods=['GET'])
def test_prompt():
    country = request.args.get('country')
    language = request.args.get('language')
    session = request.args.get('session')

    if not all([country, language, session]):
        return jsonify({"error": "Missing required query parameters"}), 400

    instructions = get_prompt_instructions(country, language, session, {})
    return jsonify(instructions)

@mcp_bp.route('/mcp/getAvailableLanguages', methods=['GET'])
def available_languages():
    country = request.args.get('country')
    if not country:
        return jsonify({"error": "Missing country query parameter"}), 400

    languages = get_available_languages(country)
    return jsonify(languages)

@mcp_bp.route('/mcp/getCountryFinancialContext', methods=['GET'])
def country_financial_context():
    country = request.args.get('country')
    if not country:
        return jsonify({"error": "Missing country query parameter"}), 400

    context = get_country_financial_context(country)
    return jsonify(context)
