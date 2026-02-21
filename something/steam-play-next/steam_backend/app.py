from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import re
import html

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Steam Proxy Enhanced is Running!"

# 1. 获取游戏列表 (和以前一样)
@app.route('/get_games', methods=['GET'])
def get_games():
    api_key = request.args.get('api_key')
    steam_id = request.args.get('steam_id')
    
    if not api_key or not steam_id:
        return jsonify({'error': 'Missing params'}), 400

    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        'key': api_key, 'steamid': steam_id, 'format': 'json',
        'include_appinfo': True, 'include_played_free_games': True
    }
    
    try:
        res = requests.get(url, params=params, timeout=10)
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 2. 【新增】获取游戏详情 (简介)
@app.route('/get_game_details', methods=['GET'])
def get_game_details():
    appid = request.args.get('appid')
    if not appid:
        return jsonify({'error': 'Missing appid'}), 400
        
    # l=schinese 请求中文数据
    url = "https://store.steampowered.com/api/appdetails"
    params = {'appids': appid, 'l': 'schinese'}
    
    try:
        res = requests.get(url, params=params, timeout=5)
        data = res.json()
        
        # 提取简介逻辑
        desc = "暂无简介"
        if str(appid) in data and data[str(appid)]['success']:
            raw_desc = data[str(appid)]['data'].get('short_description', '暂无简介')
            # 清洗 HTML 标签
            clean_desc = re.sub('<[^<]+?>', '', raw_desc)
            desc = html.unescape(clean_desc)
            
        return jsonify({'description': desc})
    except Exception as e:
        return jsonify({'description': "简介获取失败"}), 200 # 失败也返回200，不影响主流程

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
