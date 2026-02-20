# 这是一个 Streamlit 的示例（需要 pip install streamlit）
import streamlit as st
import requests
import random

st.title("Steam 游戏随机抽取器 🎲")

api_key = st.text_input("请输入 Steam API Key", type="password")
steam_id = st.text_input("请输入 Steam ID (64位)")
n = st.number_input("抽取数量", min_value=1, value=3)

if st.button("开始抽取"):
    if not api_key or not steam_id:
        st.error("请填写完整信息")
    else:
        # 这里放入之前的 get_user_games 函数逻辑...
        # 显示结果用 st.write(game['name'])
        pass
