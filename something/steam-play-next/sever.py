from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
# 允许跨域请求，这样你的 github.io 才能访问这个后端
CORS(app)

@app.route('/')
def home():
    return "Steam Proxy Server is Running!"

@app.route('/api/get_games', methods=['GET'])
def get_games():
    api_key = request.args.get('api_key')
    steam_id = request.args.get('steam_id')

    if not api_key or not steam_id:
        return jsonify({'error': 'Missing API Key or Steam ID'}), 400

    steam_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        'key': api_key,
        'steamid': steam_id,
        'format': 'json',
        'include_appinfo': True,
        'include_played_free_games': True
    }

    try:
        response = requests.get(steam_url, params=params, timeout=10)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
