import requests, re, time
from bs4 import BeautifulSoup

class ScrapigHandler:
    def __init__(self) -> None:
        pass

    def format_date(self, num) -> str:
        num = str(f"{num:02}")
        return num
        
    def delete_space(self, passed :str) -> str:
        passed = passed.replace(" ","")
        passed = re.sub(r"\n","",passed)
        passed = re.sub(r"\r","",passed)
        passed = re.sub(r"\xa0","",passed)
        return passed
        
    def req_soup(self, date :dict) -> BeautifulSoup:
        year = date["year"]
        month = self.format_date(date["month"])
        date = self.format_date(date["day"])
        try:
            res = requests.get(f"https://tenki.jp/past/{year}/{month}/{date}/weather/3/16/")
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                return soup
            else:
                print("対象ページがエラーっぽい…日付間違えてないか再度確認を")
                return
        except:
            print("対象ページにアクセスできないっぽい…")
            return
    
    def get_info(self, soup) -> dict:
        date = soup.select_one("#main-column > section > section:nth-child(7) > h3 > span")
        date = self.delete_space(date.text)

        tennki = soup.select_one("#past-live-area-pref-list-entries > tr:nth-child(2) > td.weather-telop-entry")
        tennki = self.delete_space(tennki.text)

        saikoukionn = soup.select_one("#past-live-area-pref-list-entries > tr:nth-child(2) > td.max-temp-entry")
        saikoukionn = self.delete_space(saikoukionn.text)

        saiteikionn = soup.select_one("#past-live-area-pref-list-entries > tr:nth-child(2) > td.min-temp-entry")
        saiteikionn = self.delete_space(saiteikionn.text)

        kousuiryou = soup.select_one("#past-live-area-pref-list-entries > tr:nth-child(2) > td.precip-entry")
        kousuiryou = self.delete_space(kousuiryou.text)
        
        data = {"date":date, "tennki":tennki, "saikoukionn":saikoukionn, "saiteikionn":saiteikionn, "kousuiryou":kousuiryou}
        return data


    def run(self, date_dic :dict) -> dict:
        time.sleep(0.5)
        soup = self.req_soup(date_dic)
        if soup:
            data = self.get_info(soup)
            return data
        

'''
目次
show_data               :データをプリント
data_exists             :特定のデータが存在しているかを先にverify
insert_data             :上と連携して、データinsert時に重複があった場合はスキップできる関数
insert_data_hard        :重複データの有無関係なくinsertする関数
select_data             :データを戻り値としてselectする関数。該当するのは全て出てくる
select_one_data         :上に対して、一つのみselectしてくれるモノ
count_data              :対象テーブルにどれだけデータが格納されてるかをintで返す
get_columns             :対象テーブルのカラムを返す
'''


import sqlite3
import settings


######
#以下がデフォルトの接続先DB
db_path = settings.db_path
######

class DBHandler:

    def __init__(self, db_path):
        self.db_path = db_path
        #print(f"connecting to {self.db_path}")

    def show_data(self, table_name):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        sql_select = f'SELECT * FROM {table_name};'
        cur.execute(sql_select)

        #print(get_columns(table_name))
        for r in cur:
            print(r)

        conn.close()

    def data_exists(self, table, data, check_columns=None):
        """
        同様のデータが存在しているか確認
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # Determine which columns to check
        if check_columns is None:
            check_columns = data.keys()

        # Create the query to check for existing data
        query = f"SELECT * FROM {table} WHERE " + " AND ".join([f"{k} = ?" for k in check_columns])

        # Prepare the values for the columns to be checked
        check_values = [data[k] for k in check_columns]

        cur.execute(query, tuple(check_values))
        exists = cur.fetchone() is not None

        conn.close()
        return exists

    def insert_data(self, table, data, check_columns=None):
        """
        check_columnsで指定されたカラムを対象に、すでに同様のデータがあるかどうかを確認し、なければデータを挿入する
        """
        # Check if the data already exists based on specific columns
        if self.data_exists(table, data, check_columns):
            print("Data already exists with specified columns, skipping insert.")
            return 1

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # Create the column names for the INSERT
        columns = ",".join(data.keys())

        # Create the placeholders for VALUES
        values = ",".join(["?"] * len(data))

        query = f"INSERT INTO {table} ({columns}) VALUES ({values});"

        cur.execute(query, tuple(data.values()))

        conn.commit()
        conn.close()

    def insert_data_hard(self, table, data):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # Create the column names for the INSERT
        columns = ",".join(data.keys())

        # Create the placeholders for VALUES
        values = ",".join(["?"] * len(data))

        query = f"INSERT INTO {table} ({columns}) VALUES ({values});"

        cur.execute(query, tuple(data.values()))

        conn.commit()
        conn.close()

    def select_data(self, table_name, conditions=None, fields=None):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        query = f"SELECT {fields or '*'} FROM {table_name}"
        if conditions:
            query += f" WHERE {conditions}"
            
        cur.execute(query)
        records = cur.fetchall()
        
        conn.close()
        
        return records

    def select_one_data(self, table_name, conditions=None, fields=None):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        query = f"SELECT {fields or '*'} FROM {table_name}"
        if conditions:
            query += f" WHERE {conditions}"
        query += f" LIMIT 1"
            
        cur.execute(query)
        record = cur.fetchone()  # fetchone を使用して1つのレコードのみを取得
        
        conn.close()
        
        if record:
            if len(record) == 1:  # 結果が1つのフィールドのみの場合
                return record[0]  # 最初のフィールドの値を返す
            else:
                return record
        else:
            return None  # 結果がない場合は None を返す
    
    def count_data(self, table_name):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        sql_select = f'SELECT COUNT(*) FROM {table_name};'
        cur.execute(sql_select)

        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return 0
    
    def get_columns(self, table_name):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(f"PRAGMA table_info({table_name});")
        columns = [tup[1] for tup in c.fetchall()]
        conn.close()
        return columns
    
###########################
    
import streamlit as st
import pandas as pd


class ClimateArea:
    def __init__(self, db_path :str) -> None:
        self.db_path = db_path
        self.db_handle = DBHandler(db_path)

    def get_date_dic(self, year, month, day):
        date_dic = {}
        date_dic["year"] = int(year)
        date_dic["month"] = int(month)
        date_dic["day"] = int(day)
        return date_dic

    def get_climate_info(self, date_dic :dict) -> dict:
        data = ScrapigHandler().run(date_dic)
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
            date_dic = tommorow(date_dic)
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
            date_dic = tommorow(date_dic)
            df = pd.DataFrame(data_taple_list, columns = columns)
        st.table(df)

################################

db_path = settings.db_path

#####

schema = settings.screen_time_table_schema

#####

def create_table(schema, table_name = None, db_path = None):
    """
    与えられたカラムとテーブル名に従ってDBに新たにテーブルを作るための関数
    """
    if db_path == None:
        db_path = settings.db_path

    if table_name == None:
        table_name = schema["table_name"]
    columns = schema["columns"]

    columns_sql = ", ".join([f"{col['name']} {col['type']}" for col in columns])
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(create_table_sql)

    conn.commit()
    conn.close()

create_table(schema)

#########################

month_day_list = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def tommorow(date):
    year = int(date["year"])
    month = int(date["month"])
    day = int(date["day"])

    if year % 4 == 0:
        month_day_list[2] = 29
    if year % 100 == 0:
        month_day_list[2] = 28
    if year % 400 == 0:
        month_day_list[2] = 29

    day += 1

    if day == month_day_list[month] + 1:
        month += 1
        day = 1
    elif day > month_day_list[month] + 1:
        print("?????")
        return

    if month  ==  13:
        year += 1
        month = 1
        day = 1

    date = {}
    date["year"] = year
    date["month"] = month
    date["day"] = day

    return date