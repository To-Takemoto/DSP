import pandas as pd
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

        for i in range(span):
            nth = 1
            date_str_screen = f"{date_dic['year']}年{date_dic['month']}月{date_dic['day']}日"
            data_tuple = utils.DBHandler(settings.db_path).select_one_data("screen_time_table", f"date = '{date_str_screen}'")
            for type_ in result_list:
                try:
                    data = data_tuple[nth].replace("2024年","")
                    data = data_tuple[nth].replace("2023年","")
                except AttributeError:
                    data = data_tuple[nth]
                type_.append(data)
                nth += 1
            date_dic = tommorow.tommorow(date_dic)

        dataset = pd.DataFrame(result_list[1:], 
                       columns = date_list, 
                       index = ("SNS", "エンターテイメント", "情報と読書", "その他", "クリエイティビティ",
                             "仕事効率化", "ショッピング", "ユーティリティ", "ゲーム"))
        
        return dataset
    
    def draw_screen_time_graph(self, dataset:pd.DataFrame) -> None:
        #https://qiita.com/s_fukuzawa/items/6f9c1a3d4c4f98ae6eb1
        #この関数のスクリプトは上より引用
        fig, ax = plt.subplots(figsize=(10, 8))
        for i in range(len(dataset)):
            ax.bar(dataset.columns, dataset.iloc[i], bottom=dataset.iloc[:i].sum())
        ax.set(xlabel='日付', ylabel='時間(分)')
        ax.legend(dataset.index)
        plt.show()

    def draw_temperature_graph(self, date_dic: dict, span: int, target: int) -> None:
        result_list = []
        date_list = []
        db_handle = utils.DBHandler(settings.db_path)
        for i in range(span):
            date_str_climate = self.get_date_str_climate(date_dic)
            data_tuple = db_handle.select_one_data("climate_table", f"date = '{date_str_climate}'")
            
            # 気温データを数値に変換
            try:
                result = float(data_tuple[target].replace('℃', ''))
            except ValueError:
                result = None  # 数値に変換できない場合はNoneを設定
            
            if result is not None:
                result_list.append(result)

            date = data_tuple[1]
            date = self.format_date(date)
            date_list.append(date)
            date_dic = tommorow.tommorow(date_dic)

        date_list = [datetime.strptime(date, "%Y-%m-%d") for date in date_list]

        plt.figure(figsize=(10, 5))
        plt.plot(date_list, result_list, marker='o')

        # X軸を日付フォーマットに設定
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        plt.gcf().autofmt_xdate()  # X軸のラベルを見やすくする

        plt.title('Daily Maximum Temperatures')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.grid(True)
        plt.show()