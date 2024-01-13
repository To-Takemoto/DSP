import scraping_v1 as scr
import utils, tommorow
import streamlit as st
import pandas as pd


class ClimateArea:
    def __init__(self, db_path :str) -> None:
        self.db_path = db_path
        self.db_handle = utils.DBHandler(db_path)

    def get_date_dic(self, year, month, day):
        date_dic = {}
        date_dic["year"] = int(year)
        date_dic["month"] = int(month)
        date_dic["day"] = int(day)
        return date_dic

    def get_climate_info(self, date_dic :dict) -> dict:
        data = scr.ScrapigHandler().run(date_dic)
        return data
    
    def insert_climate_data(self, data :dict) -> None:
        check_columns = ["date"]
        a = self.db_handle.insert_data("climate_table", data, check_columns)
        if a:
            date = data["date"]
            st.write(f"{date}のお天気データがすでに存在してるっぽい…")


    def get_date_str_climate(self, date_dic:dict) -> str:
        year = date_dic["year"]
        month = date_dic["month"]
        day = date_dic["day"]
        month_ = f"{month:02}"
        day_ = f"{day:02}"
        date_str_climate = f"{year}年{month_}月{day_}日"
        return date_str_climate

    def collect_climate_data(self, date_dic :dict, span :int):
        for i in range(span):
            data = self.get_climate_info(date_dic)
            self.insert_climate_data(data)
            date_dic = tommorow.tommorow(date_dic)
            if data == None:
                st.write("データないっぽい…未来のデータ参照しようとしてないかい")
                break

    def show_data(self, date_dic :dict, span :int):
        data_taple_list = []
        for i in range(span):
            date_str_climate = self.get_date_str_climate(date_dic)
            data_tuple = self.db_handle.select_one_data("climate_table", f"date = '{date_str_climate}'")
            if data_tuple == None:
                st.write(f"{date_str_climate}以降のデータが存在しないっぽい…")
                break
            data_taple_list.append(data_tuple)
            columns = self.db_handle.get_columns("climate_table")
            date_dic = tommorow.tommorow(date_dic)
            df = pd.DataFrame(data_taple_list, columns = columns)
        st.table(df)