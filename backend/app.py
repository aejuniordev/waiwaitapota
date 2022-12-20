import os

from flask import Flask, request, jsonify
from flask_cors import CORS  # to avoid cors error in different frontend like react js or any other

from routes.palavras import palavra
from routes.usuarios import usuario 


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def hello():
    return {"hello": "world"}, 200

@app.errorhandler(404)
def not_found(error=None):
    return {'error': 'Not found'}, 404

app.register_blueprint(palavra, url_prefix='/palavras')
app.register_blueprint(usuario, url_prefix='/usuarios')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port,use_reloader=True )