from flask import Flask
from mcp_server.routes import mcp_bp

app = Flask(__name__)
app.register_blueprint(mcp_bp)

if __name__ == '__main__':
    app.run(debug=True)
