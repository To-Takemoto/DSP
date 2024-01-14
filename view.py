import streamlit as st
import scr, settings

# サイドバーにラジオボタンを設置
page = st.sidebar.radio("ページを選択", ("ホーム", "ローカルデータ挿入", "グローバルデータ採集,表示"))

st.title("DSP最終課題")

# ホームページの内容
if page == "ホーム":
    
    st.header("about")
    st.write("データをinsertする時に毎回コードを書き換えるのも億劫なので、streamlitを使用してGUIにした")
    st.header("使い方")
    st.write("左のサイドメニューからやりたい項目を選んでください")
    st.write("insert_local_data.py : ローカルデータをDBに格納するためのページ")
    st.write("global_data.py : スクレイピングをしたり、スクレイピングで得たデータを表示するページ")

# ページ1の内容
elif page == "グローバルデータ採集,表示":
    area_handle = scr.ClimateArea(settings.db_path)

    st.header("DSP最終課題 グローバルデータマネージャ")
    year = st.text_input("年")
    month = st.text_input("月")
    day = st.text_input("日付")
    span = st.text_input("スパン")

    if st.button("データの新規挿入"):
        span = int(span)
        date_dic = area_handle.get_date_dic(year, month, day)
        area_handle.collect_climate_data(date_dic, span)

    if st.button("既存のデータ表示"):
        span = int(span)
        date_dic = area_handle.get_date_dic(year, month, day)
        area_handle.show_data(date_dic, span)

# ページ2の内容
elif page == "ローカルデータ挿入":
    st.header("DSP最終課題 ローカルデータマネージャ")
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

    if st.button("入力が終わったらこのボタンを押して格納"):

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
            scr.DBHandler(settings.db_path).insert_data("screen_time_table", result_dic, check_list)
            st.write("Done!")
        except ValueError:
            st.write("年月が空欄かも…")