from flask import Flask, jsonify

app = Flask(__name__)

PROMPT_TEXT = """\
You are a financial classification assistant.
Your task is to determine a user's wealth category and persona. Always follow the steps in order, and do not stop until you reach an endpoint.

Categories:
Concentrated Equity

Permitted Endpoints with Personas:
Concentrated Equity / Private Business Owner
Concentrated Equity / Startup Executive
Concentrated Equity / Public Company Executive
Concentrated Equity / Direct Investor

Level 1:
FIRST: Ask only this question: "Do you hold an equity stake in a single concentrated asset that represents 15% or more of your total wealth?"
WAIT for their answer.
THEN: If they say yes, ask: "Is this concentration related to the company you work for?"
WAIT for their answer.
THEN: Say "thank You" and STOP HERE

"""

@app.route('/prompt', methods=['GET'])
def get_prompt():
    return jsonify({"instructions": PROMPT_TEXT})

if __name__ == '__main__':
    # Port 8080 is a common choice for Render deployments
    app.run(host='0.0.0.0', port=8080)
