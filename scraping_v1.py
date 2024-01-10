import requests, re
from bs4 import BeautifulSoup
import settings, utils

class ScrapigHandler:
    def __init__(self, date:dict) -> None:
        self.year = date["year"]
        self.month = self.format_date(date["month"])
        self.date = self.format_date(date["date"])

    def format_date(self, num) -> dict:
        num = str(f"{num:0{2}}")
        return num
        
    def delete_space(self, passed:str) -> str:
        passed = passed.replace(" ","")
        passed = re.sub(r"\n","",passed)
        passed = re.sub(r"\r","",passed)
        passed = re.sub(r"\xa0","",passed)
        return passed
        
    def req_soup(self) -> BeautifulSoup:
        try:
            res = requests.get(f"https://tenki.jp/past/{self.year}/{self.month}/{self.date}/weather/3/16/")
            if res.status_code == 200:
                self.soup = BeautifulSoup(res.text, 'html.parser')
            else:
                print("対象ページがエラーっぽい…日付間違えてないか再度確認を")
        except:
            print("対象ページにアクセスできないっぽい…")
    
    def get_info(self) -> dict:
        soup = self.soup

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
        
        self.data = {"date":date, "tennki":tennki, "saikoukionn":saikoukionn, "saiteikionn":saiteikionn, "kousuiryou":kousuiryou}
    
    def insert_data(self) -> None:
        check_list = ["date"]
        utils.DBHandler(db_path = settings.db_path).insert_data("climate_table", self.data, check_list)

    def run(self) -> None:
        self.req_soup()
        self.get_info()
        self.insert_data()