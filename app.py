import os
from flask import Flask, send_from_directory, jsonify

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
STATIC_DIR = PUBLIC_DIR if os.path.exists(PUBLIC_DIR) else BASE_DIR

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='')

@app.route('/')
def index():
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "Vitoniya Global Technologies Web Service",
        "domain": "vitoniya.com"
    }), 200

@app.route('/favicon.ico')
def favicon():
    # Return SVG favicon if requested as .ico
    return send_from_directory(STATIC_DIR, 'favicon.svg', mimetype='image/svg+xml')

@app.errorhandler(404)
def not_found(e):
    return send_from_directory(STATIC_DIR, 'index.html'), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
