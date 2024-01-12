import streamlit as st
import utils, settings

st.title("DSP最終課題")
year = st.text_input("年")
month = st.text_input("月")
date = st.text_input("日付")

sns = st.text_input("SNS(分)")
Entame = st.text_input("エンターテイメント(分)")
Zyouhou = st.text_input("情報と読書(分)")
Sonohoka = st.text_input("その他(分)")
Creatibity = st.text_input("クリエイティビティ(分)")
Sigoto = st.text_input("仕事効率化(分)")
Shopping = st.text_input("ショッピング(分)")
Util = st.text_input("ユーティリティ(分)")
Game = st.text_input("ゲーム(分)")

if st.button("a"):

    result_list = (sns, Entame, Zyouhou, Sonohoka, Creatibity, Sigoto, Shopping, Util, Game)
    type_list = ("SNS", "Entame", "Zyouhou", "Sonohoka", "Creatibity", "Sigoto", "Shopping", "Util", "Game")
    result_list_int = []

    for result in result_list:
        if result == "":
            result = 0
        else:
            result = int(result)
        result_list_int.append(result)
        
    try:
        date = f"{int(year)}年{int(month)}月{int(date)}日"
        result_dic = dict(zip(type_list, result_list_int))
        result_dic = result_dic | {"date":date}
        check_list = ["date"]
        utils.DBHandler(settings.db_path).insert_data("screen_time_table", result_dic, check_list)
        st.write("Done!")
    except ValueError:
        st.write("年月が空欄かも…")
        
    

    