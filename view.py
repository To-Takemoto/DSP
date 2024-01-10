import streamlit as st
import utils, settings
db_handle = utils.DBHandler(settings.db_path)

st.title("a")

year = st.text_input("年")
month = st.text_input("月")
date = st.text_input("日付")

if st.button("aaa"):
    date = f"{year}年{month}月{date}日"
    a = db_handle.select_one_data("climate_table", f"date = '{date}'", "*")
    print(a)    