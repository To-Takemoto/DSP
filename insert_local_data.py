import streamlit as st
import utils

st.title("DSP最終課題")
year = st.text_input("年")
month = st.text_input("月")
date = st.text_input("日付")

sns = st.text_input("SNS")
Entame = st.text_input("Entame")
Zyouhou = st.text_input("Zyouhou")
Sonohoka = st.text_input("Sonohoka")
Creatibity = st.text_input("Creatibity")
Sigoto = st.text_input("Sigoto")
Shopping = st.text_input("Shopping")
Util = st.text_input("Util")
Game = st.text_input("Game")

if st.button("a"):

    result_list = (sns, Entame, Zyouhou, Sonohoka, Creatibity, Sigoto, Shopping, Util, Game)
    type_list = ("SNS", "Entame", "Zyouhou", "Sonohoka", "Creatibity", "Sigoto", "Shopping", "Util", "Game")
    result_list_int = []

    for result in result_list:
        result = int(result)
        result_list_int.append(result)

    date = f"{year}年{month}月{date}日"
    
    result_dic = dict(zip(type_list, result_list_int))
    result_dic = result_dic | {"date":date}

    check_list = ["date"]
    utils.DBHandler().insert_data("screen_time_table", result_dic, check_list)
    