# 文件路径: something/steam-play-next/backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app) # 允许跨域，这对 github.io 很重要

@app.route('/')
def home():
    return "Steam Proxy is Running!"

@app.route('/get_games', methods=['GET'])
def get_games():
    api_key = request.args.get('api_key')
    steam_id = request.args.get('steam_id')

    if not api_key or not steam_id:
        return jsonify({'error': 'Missing params'}), 400

    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        'key': api_key, 
        'steamid': steam_id, 
        'format': 'json',
        'include_appinfo': True, 
        'include_played_free_games': True
    }
    
    try:
        res = requests.get(url, params=params, timeout=10)
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
