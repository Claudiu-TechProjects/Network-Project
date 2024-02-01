from flask import request, Flask,send_from_directory

app = Flask(__name__)


@app.route('/')
def serve_html():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)