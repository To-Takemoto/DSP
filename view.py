import streamlit as st
import back_engine as be
import settings

area_handle = be.ClimateArea(settings.db_path)

st.title("DSP最終課題")
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