import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import utils, settings, tommorow
plt.rcParams['font.family'] = 'IPAexGothic'
sns.set(font='IPAexGothic')

class TinkingGraph:
    def __init__(self, db_path = None) -> None:
        if db_path == None:
            self.db_path = settings.db_path
        else:
            self.db_path = db_path

    def format_date(self, date_str_climate:str) -> str:
        date = date_str_climate
        date = date.replace("年","-")
        date = date.replace("月","-")
        date = date.replace("日","")
        return date

    def get_date_str_climate(self, date_dic:dict) -> str:
        year = date_dic["year"]
        month = date_dic["month"]
        day = date_dic["day"]
        month_ = f"{month:02}"
        day_ = f"{day:02}"
        date_str_climate = f"{year}年{month_}月{day_}日"
        return date_str_climate
    
    def make_span_dataset(self, date_dic :dict, span :int) -> pd.DataFrame:

        date_list = []
        Sns = []
        Entame = []
        Zyouhou = []
        Sonohoka = []
        Creatibity = []
        Sigoto = []
        Shopping = []
        Util = []
        Game = []
        result_list = (date_list, Sns, Entame, Zyouhou, Sonohoka, Creatibity, Sigoto, Shopping, Util, Game)
        
        db_handle = utils.DBHandler(self.db_path)
        for i in range(span):
            nth = 1
            date_str_screen = f"{date_dic['year']}年{date_dic['month']}月{date_dic['day']}日"
            data_tuple = db_handle.select_one_data("screen_time_table", f"date = '{date_str_screen}'")
            for type_ in result_list:
                if nth == 1:
                    data = f"{date_dic['day']}日"
                else:
                    data = data_tuple[nth]
                type_.append(data)
                nth += 1
            date_dic = tommorow.tommorow(date_dic)

        dataset = pd.DataFrame(result_list[1:], 
                       columns = date_list, 
                       index = ("SNS", "エンターテイメント", "情報と読書", "その他", "クリエイティビティ",
                             "仕事効率化", "ショッピング", "ユーティリティ", "ゲーム"))
        
        return dataset
    
    def draw_screen_time_graph(self, dataset :pd.DataFrame) -> None:
        #https://qiita.com/s_fukuzawa/items/6f9c1a3d4c4f98ae6eb1
        #この関数のスクリプトは上より引用
        fig, ax = plt.subplots(figsize=(10, 8))
        for i in range(len(dataset)):
            ax.bar(dataset.columns, dataset.iloc[i], bottom=dataset.iloc[:i].sum())
        ax.set(xlabel='日付', ylabel='時間(分)')
        ax.legend(dataset.index)
        plt.show()

    def draw_temperature_graph(self, date_dic :dict, span :int) -> None:
        min_temp_list = self.get_climate_list(date_dic, span, 4)
        max_temp_list = self.get_climate_list(date_dic, span, 3)
        precipitation_list = self.get_climate_list(date_dic, span, 5)
        date_list = self.get_date_list(date_dic, span, 4)
        date_list = [datetime.strptime(date, "%Y-%m-%d") for date in date_list]

        fig, ax1 = plt.subplots(figsize=(10, 5))

        # 最高気温と最低気温の折れ線グラフをプロット
        ax1.plot(date_list, min_temp_list, marker='o', label='最低気温')
        ax1.plot(date_list, max_temp_list, marker='o', label='最高気温')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Temperature (°C)', color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        ax1.legend(loc='upper left')

        # 降水量の棒グラフをオーバーレイ
        ax2 = ax1.twinx()  # 同じx軸を共有する新しいy軸を作成
        ax2.bar(date_list, precipitation_list, alpha=0.5, color='gray', label='降水量')
        ax2.set_ylabel('Precipitation (mm)', color='gray')
        ax2.tick_params(axis='y', labelcolor='gray')
        ax2.legend(loc='upper right')

        # X軸を日付フォーマットに設定
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.xaxis.set_major_locator(mdates.DayLocator())
        fig.autofmt_xdate()  # X軸のラベルを見やすくする

        plt.title('日毎の気温の変遷')
        plt.grid(True)
        plt.show()

    def get_screen_time_sum_list(self, date_dic :dict, span :int):
        result_list = []
        db_handle = utils.DBHandler(self.db_path)
        for i in range(span):
            date_str_screen = f"{date_dic['year']}年{date_dic['month']}月{date_dic['day']}日"
            data_tuple = db_handle.select_one_data("screen_time_table", f"date = '{date_str_screen}'")
            sum = 0
            for data in data_tuple[2:]:
                sum += data
            result_list.append(sum)
            date_dic = tommorow.tommorow(date_dic)
        return result_list
    
    def get_date_list(self, date_dic :dict, span :int, type :int):
        result_list = []
        for i in range(span):
            if type == 1:
                date_str_screen = f"{date_dic['year']}年{date_dic['month']}月{date_dic['day']}日"
                result_list.append(date_str_screen)
            elif type == 2:
                data = self.get_date_str_climate(date_dic)
                result_list.append(data)
            elif type == 3:
                result_list.append(date_dic['day'])
            elif type == 4:
                data = self.get_date_str_climate(date_dic)
                data = self.format_date(data)
                result_list.append(data)
            date_dic = tommorow.tommorow(date_dic)
        return result_list
    
    def get_climate_list(self, date_dic :dict, span :int, target:int):
        result_list = []
        db_handle = utils.DBHandler(self.db_path)
        for i in range(span):
            date_str_climate = self.get_date_str_climate(date_dic)
            data_tuple = db_handle.select_one_data("climate_table", f"date = '{date_str_climate}'")
            data = data_tuple[target]
            try:
                data = data.replace("℃","")
                data = data.replace("mm","")
                data = float(data)
            except ValueError:
                print("データが存在しないっぽい…")
                return
            result_list.append(data)
            date_dic = tommorow.tommorow(date_dic)
        return result_list


    def draw_scatter_plot(self, date_dic :dict, span :int):
        max_temperature = self.get_climate_list(date_dic, span, 3)
        min_temperature = self.get_climate_list(date_dic, span, 4)
        screen_time = self.get_screen_time_sum_list(date_dic, span)

        correlation_min = np.corrcoef(min_temperature, screen_time)[0, 1]
        correlation_max = np.corrcoef(max_temperature, screen_time)[0, 1]

        # 散布図の作成
        plt.scatter(min_temperature, screen_time, color='blue', label='最低気温')
        plt.scatter(max_temperature, screen_time, color='red', label='最高気温')
        plt.xlabel('気温 (°C)')
        plt.ylabel('スクリーンタイム (min)')
        plt.title(f'スクリーンタイムと気温の散布図\n相関係数(最低気温): {correlation_min:.2f}, 相関係数(最高気温): {correlation_max:.2f}')
        plt.legend()
        plt.show()